import { E as EnumViews } from './EnumViews-b32e9b99.js';

const workflowSteps = [
    {
        currentView: EnumViews.recipient,
        previousView: EnumViews.home,
        nextView: EnumViews.selectFile,
        label: 'Select recipient',
    },
    {
        currentView: EnumViews.selectFile,
        previousView: EnumViews.recipient,
        nextView: EnumViews.templateRoles,
        label: 'Select document',
    },
    {
        currentView: EnumViews.templateRoles,
        previousView: EnumViews.selectFile,
        nextView: EnumViews.sendDocument,
        label: 'Connect Roles',
    },
    {
        currentView: EnumViews.sendDocument,
        previousView: EnumViews.selectFile,
        nextView: EnumViews.documentValidation,
        label: 'Prepare sendout',
    },
    {
        currentView: EnumViews.documentValidation,
        previousView: EnumViews.sendDocument,
        nextView: EnumViews.documentValidation,
        label: 'Send document',
    },
];

export { workflowSteps as w };

//# sourceMappingURL=workflow-steps-ef1ed8f2.js.map