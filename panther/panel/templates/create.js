const schema = JSON.parse('{{fields|tojson|safe}}');

function toggleObjectVisibility(checkbox, contentId) {
  const content = document.getElementById(contentId);
  content.classList.toggle('hidden', !checkbox.checked);

  // Disable/enable all inputs within the container
  const inputs = content.querySelectorAll('input, select, textarea');
  inputs.forEach((input) => {
    input.disabled = !checkbox.checked;
  });
}

function createObjectInputs(objectSchema, container, prefix = '') {
  Object.entries(objectSchema.fields).forEach(([fieldName, field]) => {
    const fullFieldName = prefix ? `${prefix}.${fieldName}` : fieldName;

    if (field.type.includes('array')) {
      // Array handling remains the same
      const itemType = field.items.replace('$', '');
      const arrayContainer = createArrayField(
        fieldName,
        itemType,
        container
      );
    } else if (field.type.some((t) => t.startsWith('$'))) {
      // Handle object type (either nullable or required)
      const objectType = field.type
        .find((t) => t.startsWith('$'))
        .replace('$', '');
      const isNullable = field.type.includes('null');

      const objectWrapper = document.createElement('div');
      objectWrapper.className = 'space-y-4';

      // Only add the toggle if it's nullable
      if (isNullable) {
        const toggleId = `${fullFieldName}_toggle`;
        const contentId = `${fullFieldName}_content`;

        const toggle = document.createElement('label');
        toggle.className = 'flex items-center space-x-3 mb-2';
        toggle.innerHTML = `
      <input type="checkbox" id="${toggleId}"
             class="form-checkbox h-5 w-5 text-blue-600 bg-gray-700 border-gray-600 rounded"
             ${!field.required ? '' : 'checked disabled'}
             onchange="toggleObjectVisibility(this, '${contentId}')">
      <span class="text-sm font-medium">Include ${field.title || fieldName
          }</span>
    `;
        objectWrapper.appendChild(toggle);
      }

      // Create the object container
      const objectContainer = document.createElement('div');
      objectContainer.id = `${fullFieldName}_content`;
      objectContainer.className =
        'border border-gray-700 p-4 rounded-lg space-y-4';

      // If nullable and not required, start hidden
      if (isNullable && !field.required) {
        objectContainer.classList.add('hidden');
      }

      objectContainer.innerHTML = `<h3 class="text-lg font-medium">${field.title || fieldName
        }</h3>`;

      // Create the nested object inputs
      const nestedSchema = schema.$[objectType];
      createObjectInputs(nestedSchema, objectContainer, fullFieldName);

      objectWrapper.appendChild(objectContainer);
      container.appendChild(objectWrapper);
    } else {
      // Basic input handling remains the same
      createBasicInput(fieldName, field, container, fullFieldName);
    }
  });
}

function createBasicInput(fieldName, field, container, fullFieldName) {
  const inputWrapper = document.createElement('div');
  inputWrapper.className = 'space-y-2';

  let inputHTML = '';
  if (field.type.includes('boolean')) {
    inputHTML = `
                <label class="flex items-center space-x-3">
                    <input type="checkbox" name="${fullFieldName}"
                           ${field.required ? 'required' : ''}
                           class="form-checkbox h-5 w-5 text-blue-600 bg-gray-700 border-gray-600 rounded">
                    <span class="text-sm font-medium">${field.title || fieldName
      }</span>
                </label>
            `;
  } else if (field.type.includes('string')) {
    inputHTML = `
                <label class="block">
                    <span class="text-sm font-medium">${field.title || fieldName}</span>
                    <input type="text" name="${fullFieldName}"
                           ${field.required ? 'required' : ''}
                           class="w-full mt-1 p-2 bg-gray-700 rounded text-gray-300">
                </label>
            `;
  } else if (field.type.includes('integer')) {
    inputHTML = `
                <label class="block">
                    <span class="text-sm font-medium">${field.title || fieldName
      }</span>
                    <input type="number" name="${fullFieldName}"
                           ${field.required ? 'required' : ''}
                           class="w-full mt-1 p-2 bg-gray-700 rounded text-gray-300">
                </label>
            `;
  }

  inputWrapper.innerHTML = inputHTML;
  container.appendChild(inputWrapper);
}

function createArrayField(fieldName, itemType, container) {
  const arrayContainer = document.createElement('div');
  arrayContainer.className =
    'border border-gray-700 p-4 rounded-lg space-y-4';

  const arrayHeader = document.createElement('div');
  arrayHeader.className = 'flex justify-between items-center mb-4';

  // Create a container for the spreadsheet with a unique ID
  const spreadsheetId = `${fieldName}-container`;

  arrayHeader.innerHTML = `
<h3 class="text-lg font-medium">${fieldName}</h3>
<button type="button" class="bg-green-600 px-3 py-1 rounded text-sm"
        onclick="addArrayRow('${fieldName}', '${itemType}', '${spreadsheetId}')">
  Add Row
</button>
`;

  const spreadsheet = document.createElement('div');
  spreadsheet.className = 'array-container flex  gap-4 overflow-auto 	py-2';
  spreadsheet.id = spreadsheetId;

  const headerRow = document.createElement('div');
  headerRow.className =
    'flex flex-col gap-4 py-2';

  const itemSchema = schema.$[itemType];
  const columns = Object.entries(itemSchema.fields);


  columns.forEach(([_, field]) => {
    const headerCell = document.createElement('div');
    headerCell.className = 'font-medium text-sm bg-gray-600 p-2 rounded min-w-24';
    headerCell.textContent = field.title || field.name;
    headerRow.appendChild(headerCell);
  });

  headerRow.appendChild(document.createElement('div'));

  spreadsheet.appendChild(headerRow);
  arrayContainer.appendChild(arrayHeader);
  arrayContainer.appendChild(spreadsheet);
  container.appendChild(arrayContainer);

  return spreadsheet;
}

function addArrayRow(arrayName, itemType, containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const itemSchema = schema.$[itemType];
  const columns = Object.entries(itemSchema.fields);

  const row = document.createElement('div');
  row.className = 'flex flex-col gap-4 py-2	';


  const rowIndex = container.children.length - 1;

  columns.forEach(([fieldName, field]) => {
    const cell = document.createElement('div');

    if (field.type.includes('boolean')) {
      cell.innerHTML = `
    <input type="checkbox"
           name="${arrayName}[${rowIndex}].${fieldName}"
           class="form-checkbox h-5 w-5 text-blue-600 bg-gray-700 border-gray-600 rounded"
           ${field.required ? 'required' : ''}>
  `;
    } else if (field.type.includes('string')) {
      cell.innerHTML = `
    <input type="text"
           name="${arrayName}[${rowIndex}].${fieldName}"
           class="w-full bg-gray-700 rounded text-gray-300 text-md p-2 min-w-64 "
           ${field.required ? 'required' : ''}>
  `;
    } else if (field.type.includes('integer')) {
      cell.innerHTML = `
    <input type="number"
           name="${arrayName}[${rowIndex}].${fieldName}"
           class="w-full bg-gray-700 rounded text-gray-300 text-md p-2  min-w-64"
           ${field.required ? 'required' : ''}>
  `;
    } else if (field.type.some((t) => t.startsWith('$'))) {
      const objectType = field.type
        .find((t) => t.startsWith('$'))
        .replace('$', '');
      cell.innerHTML = `
    <button type="button"
            class="w-full bg-blue-600 px-2 py-1 rounded text-sm"
            onclick="openObjectModal('${arrayName}[${rowIndex}].${fieldName}', '${objectType}')">
      Edit
    </button>
  `;
    }

    row.appendChild(cell);
  });

  const deleteCell = document.createElement('div');
  deleteCell.className = 'w-20'; // Width for action column
  deleteCell.innerHTML = `
    <button type="button"
        class="bg-red-600 px-2 py-1 rounded text-sm"
        onclick="this.closest('.flex').remove()">
      Delete
    </button>`;
  row.appendChild(deleteCell);
  container.appendChild(row);
}

function openObjectModal(fieldName, objectType) {
  // Create modal for editing nested object
  const modal = document.createElement('div');
  modal.className =
    'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center';
  modal.innerHTML = `
<div class="bg-gray-800 p-6 rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
  <h3 class="text-lg font-medium mb-4">Edit ${fieldName}</h3>
  <div class="object-inputs space-y-4"></div>
  <div class="mt-4 flex justify-end space-x-2">
    <button type="button" class="bg-gray-600 px-4 py-2 rounded" onclick="this.closest('.fixed').remove()">
      Cancel
    </button>
    <button type="button" class="bg-blue-600 px-4 py-2 rounded" onclick="saveObjectModal(this)">
      Save
    </button>
  </div>
</div>
`;

  const objectSchema = schema.$[objectType];
  createObjectInputs(
    objectSchema,
    modal.querySelector('.object-inputs'),
    fieldName
  );

  document.body.appendChild(modal);
}

const dynamicInputs = document.getElementById('dynamicInputs');

createObjectInputs(schema, dynamicInputs);
document
  .getElementById('createForm')
  .addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const data = {};

    for (let [key, value] of formData.entries()) {
      if (key.includes('[')) {
        // Handle array fields
        const [arrayName, index, field] = key
          .match(/([^\[]+)\[(\d+)\]\.(.+)/)
          .slice(1);
        if (!data[arrayName]) data[arrayName] = [];
        if (!data[arrayName][index]) data[arrayName][index] = {};
        data[arrayName][index][field] = value;
      } else if (key.includes('.')) {
        const [objectName, field] = key.split('.');
        if (!data[objectName]) data[objectName] = {};
        data[objectName][field] = value;
      } else {
        data[key] = value;
      }
    }

    console.log('Submitted data:', data);
  });