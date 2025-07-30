import { newSpecPage } from "@stencil/core/testing";
import { DocumentList } from "./document-list";
describe('document-list', () => {
    it('builds', async () => {
        const page = await newSpecPage({
            components: [DocumentList],
            html: '<document-list></document-list>',
        });
        expect(page.root).toBeTruthy();
    });
});
//# sourceMappingURL=document-list.spec.js.map
