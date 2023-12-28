from panther.panel.apis import Landing, ModelsAPI, DocumentsAPI

urls = {
    '_panel': Landing,
    'api/_panel/': ModelsAPI,
    'api/_panel/<index>/': DocumentsAPI,
}
