import { h } from "@stencil/core";
import { workflowSteps } from "./workflow-steps";
export class WorkflowProgressBar {
    constructor() {
        this.activeView = undefined;
        this.isVisible = undefined;
        this.changeViewHandlerPrevious =
            this.changeViewHandlerPrevious.bind(this);
        this.changeViewHandlerNext = this.changeViewHandlerNext.bind(this);
        this.changeViewSelectedStep = this.changeViewSelectedStep.bind(this);
    }
    render() {
        return (() => {
            if (this.isVisible) {
                return (h("ul", { class: "progress-steps" }, h("li", { class: "progress-action-button", onClick: this.changeViewHandlerPrevious }, "Back"), workflowSteps.map((step, index) => {
                    let progessStep = 'progress-step-icon';
                    if (step.currentView === this.activeView) {
                        progessStep += ' active';
                    }
                    return (h("li", { class: "progress-step", onClick: () => this.changeViewSelectedStep(step.currentView) }, h("span", { class: progessStep }, index + 1), h("span", { class: "progress-step-text" }, step.label)));
                }), h("li", { class: "progress-action-button", onClick: this.changeViewHandlerNext }, "Next")));
            }
        })();
    }
    changeViewHandlerPrevious() {
        const viewData = workflowSteps.find(step => {
            return step.currentView === this.activeView;
        });
        this.changeView.emit(viewData.previousView);
    }
    changeViewHandlerNext() {
        const viewData = workflowSteps.find(step => {
            return step.currentView === this.activeView;
        });
        this.changeView.emit(viewData.nextView);
    }
    changeViewSelectedStep(currentView) {
        this.changeView.emit(currentView);
    }
    static get is() { return "workflow-progress-bar"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["workflow-progress-bar.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["workflow-progress-bar.css"]
        };
    }
    static get properties() {
        return {
            "activeView": {
                "type": "string",
                "mutable": false,
                "complexType": {
                    "original": "EnumViews",
                    "resolved": "EnumViews.documentDetail | EnumViews.documentValidation | EnumViews.help | EnumViews.home | EnumViews.invite | EnumViews.login | EnumViews.logout | EnumViews.recipient | EnumViews.selectFile | EnumViews.sendDocument | EnumViews.settings | EnumViews.templateRoles | EnumViews.videoLibrary",
                    "references": {
                        "EnumViews": {
                            "location": "import",
                            "path": "../../models/EnumViews",
                            "id": "src/models/EnumViews.ts::EnumViews"
                        }
                    }
                },
                "required": false,
                "optional": false,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "attribute": "active-view",
                "reflect": false
            },
            "isVisible": {
                "type": "boolean",
                "mutable": false,
                "complexType": {
                    "original": "boolean",
                    "resolved": "boolean",
                    "references": {}
                },
                "required": false,
                "optional": false,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "attribute": "is-visible",
                "reflect": false
            }
        };
    }
    static get events() {
        return [{
                "method": "changeView",
                "name": "changeView",
                "bubbles": true,
                "cancelable": true,
                "composed": true,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "complexType": {
                    "original": "EnumViews",
                    "resolved": "EnumViews.documentDetail | EnumViews.documentValidation | EnumViews.help | EnumViews.home | EnumViews.invite | EnumViews.login | EnumViews.logout | EnumViews.recipient | EnumViews.selectFile | EnumViews.sendDocument | EnumViews.settings | EnumViews.templateRoles | EnumViews.videoLibrary",
                    "references": {
                        "EnumViews": {
                            "location": "import",
                            "path": "../../models/EnumViews",
                            "id": "src/models/EnumViews.ts::EnumViews"
                        }
                    }
                }
            }];
    }
}
//# sourceMappingURL=workflow-progress-bar.js.map
