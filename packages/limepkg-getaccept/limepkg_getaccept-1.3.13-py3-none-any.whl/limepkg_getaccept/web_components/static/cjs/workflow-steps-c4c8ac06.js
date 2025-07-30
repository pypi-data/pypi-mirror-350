'use strict';

const EnumViews = require('./EnumViews-ea9a87d2.js');

const workflowSteps = [
    {
        currentView: EnumViews.EnumViews.recipient,
        previousView: EnumViews.EnumViews.home,
        nextView: EnumViews.EnumViews.selectFile,
        label: 'Select recipient',
    },
    {
        currentView: EnumViews.EnumViews.selectFile,
        previousView: EnumViews.EnumViews.recipient,
        nextView: EnumViews.EnumViews.templateRoles,
        label: 'Select document',
    },
    {
        currentView: EnumViews.EnumViews.templateRoles,
        previousView: EnumViews.EnumViews.selectFile,
        nextView: EnumViews.EnumViews.sendDocument,
        label: 'Connect Roles',
    },
    {
        currentView: EnumViews.EnumViews.sendDocument,
        previousView: EnumViews.EnumViews.selectFile,
        nextView: EnumViews.EnumViews.documentValidation,
        label: 'Prepare sendout',
    },
    {
        currentView: EnumViews.EnumViews.documentValidation,
        previousView: EnumViews.EnumViews.sendDocument,
        nextView: EnumViews.EnumViews.documentValidation,
        label: 'Send document',
    },
];

exports.workflowSteps = workflowSteps;

//# sourceMappingURL=workflow-steps-c4c8ac06.js.map