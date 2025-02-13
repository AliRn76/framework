const fields = JSON.parse(`{{fields|tojson|safe}}`);
const fieldsObject = fields.fields;
const fieldsArray = Object.entries(fieldsObject).map(([key, value]) => ({
  title: value.title || key,
  type: value.type || [], // Default to an empty array if `type` is not defined
  required: value.required || false, // Default to `false` if `required` is not defined
}));
function pythonToJSON(str) {
  return str
    .replace(/'/g, '"')
    .replace(/False/g, "false")
    .replace(/True/g, "true")
    .replace(/None/g, "null");
}

function getDataType(value) {
  if (value === null) return "null";
  if (Array.isArray(value)) return "array";
  return typeof value;
}

function formatValue(value, type) {
  if (value === null) return '<span class="text-gray-400">null</span>';

  const accordionId = `accordion-${Math.random().toString(36).substr(2, 9)}`;

  switch (type) {
    case "array":
      return `
            <div class="w-full">
                <details class="bg-gray-700 rounded-lg max-w-[300px]">
                    <summary class="cursor-pointer px-4 py-2 text-sm font-medium text-gray-300 hover:bg-gray-600 rounded-lg flex items-center justify-between">
                        <span>Array (${value.length} items)</span>
                        <svg class="w-4 h-4 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                        </svg>
                    </summary>
                    <div class="px-4 py-2 border-t border-gray-600">
                        ${value
                          .map(
                            (item, index) => `
                            <div class="py-1 text-sm text-gray-300">
                                <span class="text-gray-400">[${index}]:</span>
                                ${formatValue(item, getDataType(item))}
                            </div>
                        `
                          )
                          .join("")}
                    </div>
                </details>
            </div>
        `;
    case "object":
      return `
            <div class="w-full max-w-[300px]">
                <details class="bg-gray-700 rounded-lg">
                    <summary class="cursor-pointer px-4 py-2 text-sm font-medium text-gray-300 hover:bg-gray-600 rounded-lg flex items-center justify-between">
                        <span>Object (${Object.keys(value).length} props)</span>
                        <svg class="w-4 h-4 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                        </svg>
                    </summary>
                    <div class="px-4 py-2 border-t border-gray-600">
                        ${Object.entries(value)
                          .map(
                            ([key, val]) => `
                            <div class="py-1 text-sm text-gray-300">
                                <span class="text-gray-400">${key}:</span>
                                ${formatValue(val, getDataType(val))}
                            </div>
                        `
                          )
                          .join("")}
                    </div>
                </details>
            </div>
        `;
    case "boolean":
      return `<span class="px-2 py-1 rounded ${
        value ? "bg-green-500/20 text-green-400" : "bg-red-500/20 text-red-400"
      }">${value}</span>`;
    default:
      return `<span class="text-sm ${
        typeof value === "string" ? "font-mono" : ""
      }">${value}</span>`;
  }
}

function toggleDropdown(button) {
  const dropdown = button.nextElementSibling;
  const allDropdowns = document.querySelectorAll(
    ".relative.inline-block .absolute"
  );

  // Close all other dropdowns
  allDropdowns.forEach((d) => {
    if (d !== dropdown) d.classList.add("hidden");
  });

  // Toggle current dropdown
  dropdown.classList.toggle("hidden");

  // Close dropdown when clicking outside
  const closeDropdown = (e) => {
    if (!button.contains(e.target) && !dropdown.contains(e.target)) {
      dropdown.classList.add("hidden");
      document.removeEventListener("click", closeDropdown);
    }
  };

  document.addEventListener("click", closeDropdown);
}

function renderTable() {
  const thead = document.getElementById("tableHead");
  const records = Array.from(document.querySelectorAll(".record-data")).map(
    (item) => JSON.parse(pythonToJSON(item.textContent.trim()))
  );
  if (records) {
    const firstRecord = records[0];
    const headers = Object.entries(firstRecord).map(([key, value]) => ({
      key,
      type: getDataType(value),
    }));
    thead.innerHTML = `
    <tr>
        ${headers
          .map(
            (field) => `
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                ${field.key} (${field.type})
            </th>
        `
          )
          .join("")}
    </tr>
`;
  }

  if (records.length > 0) {
    const firstRecord = records[0];

    const headers = Object.entries(firstRecord).map(([key, value]) => ({
      key,
      type: getDataType(value),
    }));
    console.log(headers);
    console.log(fieldsArray);
    document.querySelectorAll(".record-row").forEach((row, index) => {
      const record = records[index];
      row.innerHTML = headers
        .map(
          ({ key, type }) => `
            <td class="px-6 py-4">
                ${formatValue(record[key], type)}
            </td>
        `
        )
        .join("");
    });
  }
}

renderTable();
function getCurrentTableIndex() {
  const path = window.location.pathname;
  const match = path.match(/\/admin\/(\d+)/);
  return match ? parseInt(match[1]) : 0;
}

function selectTable(element) {
  const index = element.dataset.index;
  // Only update URL if it's different from current
  if (index !== getCurrentTableIndex().toString()) {
    window.location.href = `/admin/${index}`;
  }
}

// Set active table based on URL
function setActiveTableFromUrl() {
  const currentIndex = getCurrentTableIndex();
  const tableItems = document.querySelectorAll(".table-item");

  tableItems.forEach((item) => {
    item.classList.remove("bg-blue-600");
    item.classList.add("bg-gray-700");

    if (parseInt(item.dataset.index) === currentIndex) {
      item.classList.remove("bg-gray-700");
      item.classList.add("bg-blue-600");
    }
  });
}

// Initialize based on URL
document.addEventListener("DOMContentLoaded", () => {
  setActiveTableFromUrl();
});
