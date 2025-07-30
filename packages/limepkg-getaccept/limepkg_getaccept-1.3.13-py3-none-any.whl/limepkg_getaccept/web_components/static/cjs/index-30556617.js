'use strict';

require('./index-1129c609.js');

/**
 * Core platform service names
 * @public
 * @group Core
 */
const PlatformServiceName = {
    Route: 'route',
};

const SERVICE_NAME$m = 'state.limetypes';
PlatformServiceName.LimeTypeRepository = SERVICE_NAME$m;

/******************************************************************************
Copyright (c) Microsoft Corporation.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
***************************************************************************** */

function __decorate(decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
}

typeof SuppressedError === "function" ? SuppressedError : function (error, suppressed, message) {
    var e = new Error(message);
    return e.name = "SuppressedError", e.error = error, e.suppressed = suppressed, e;
};

const SERVICE_NAME$l = 'state.limeobjects';
PlatformServiceName.LimeObjectRepository = SERVICE_NAME$l;

/**
 * Events dispatched by the commandbus event middleware
 * @public
 * @group Command bus
 */
var CommandEventName;
(function (CommandEventName) {
    /**
     * Dispatched when the command has been received by the commandbus.
     * Calling `preventDefault()` on the event will stop the command from being handled
     *
     * @see {@link CommandEvent}
     */
    CommandEventName["Received"] = "command.received";
    /**
     * Dispatched when the command has been handled by the commandbus
     *
     * @see {@link CommandEvent}
     */
    CommandEventName["Handled"] = "command.handled";
    /**
     * Dispatched if an error occurs while handling the command
     *
     * @see {@link CommandEvent}
     */
    CommandEventName["Failed"] = "command.failed";
})(CommandEventName || (CommandEventName = {}));
/**
 * Register a class as a command
 *
 * @param options - a CommandOptions object containing the id of the command
 *
 * @returns callback which accepts a `CommandClass` and sets the command id
 * @public
 * @group Command bus
 */
function Command(options) {
    return (commandClass) => {
        setCommandId(commandClass, options.id);
        setHasInstance(commandClass, options.id);
    };
}
function setCommandId(commandClass, id) {
    // eslint-disable-next-line @typescript-eslint/dot-notation
    commandClass['commandId'] = id;
}
function setHasInstance(commandClass, id) {
    Object.defineProperty(commandClass, Symbol.hasInstance, {
        value: (instance) => {
            return getCommandIds(instance).includes(id);
        },
    });
}
/**
 * Get the registered id of the command
 *
 * @param value - either a command or a command identifier
 *
 * @returns id of the command
 * @public
 * @group Command bus
 */
function getCommandId(value) {
    if (typeof value === 'string') {
        return value;
    }
    /* eslint-disable @typescript-eslint/dot-notation */
    if (value && value.constructor && value.constructor['commandId']) {
        return value.constructor['commandId'];
    }
    if (value && value['commandId']) {
        return value['commandId'];
    }
    /* eslint-enable @typescript-eslint/dot-notation */
    return null;
}
/**
 * Get all registered ids of a command and its parent classes
 *
 * @param value - either a command or a command identifier
 *
 * @returns ids of the command
 * @beta
 * @group Command bus
 */
function getCommandIds(value) {
    let ids = [];
    let id;
    let commandClass = value;
    while ((id = getCommandId(commandClass))) {
        ids = [...ids, id];
        commandClass = Object.getPrototypeOf(commandClass);
    }
    return Array.from(new Set(ids));
}

const SERVICE_NAME$k = 'commandBus';
PlatformServiceName.CommandBus = SERVICE_NAME$k;

/**
 * Open a dialog for bulk creating limeobjects
 *
 *
 * ### Flow example
 * Let's have a look at the general flow by going through the concrete example of adding several persons to a marketing activity:
 * - Go to the table view of persons.
 * - Filter everyone who should be included in the marketing activity.
 * - Select 'Bulk create objects' form the action menu.
 * - Fill out the form and click 'create'.
 * - A toast message appears and gives you 5 seconds to undo the action before it creates the corresponding task.
 * - Another toast message will inform you after the task is completed.
 * - If the task ended successful you can go to the participant table view and check the result.
 *
 * ### Configuration
 * In order to activate the feature go to a table configuration in lime-admin to the limetype you want to bulk create from
 * and add the following configuration:
 *
 * ```json
 * "actions": [
 * {
 *      "id": "limeobject.bulk-create-dialog",
 *      "params": {
 *        "relation": "<name of relation>"
 *      }
 *    }
 * ],
 * ```
 *
 * @id `limeobject.bulk-create-dialog`
 * @public
 * @group Lime objects
 */
let BulkCreateDialogCommand = class BulkCreateDialogCommand {
    constructor() {
        /**
         * A list of relation names that are possible to create from the limetype
         *
         * @deprecated The dialog no longer supports multiple relations to be
         * picked from. Use the new {@link BulkCreateDialogCommand.relation}
         * property instead
         */
        this.relations = [];
    }
};
BulkCreateDialogCommand = __decorate([
    Command({
        id: 'limeobject.bulk-create-dialog',
    })
], BulkCreateDialogCommand);

/**
 * Open a dialog for creating a new limeobject or editing a specific limeobject
 *
 * The create dialog is implemented as a command so a plugin can easily replace the original dialog with a custom one.
 * Check out the "Hello, Event!" tutorial for a detailed description on how to implement your own create dialog.
 *
 * This dialog also useful to edit a limeobject that already exists
 *
 * @id `limeobject.create-dialog`
 * @public
 * @group Lime objects
 */
let CreateLimeobjectDialogCommand = class CreateLimeobjectDialogCommand {
    constructor() {
        /**
         * Specifies if routing to limeobject should be done after confirmation
         */
        this.route = false;
    }
};
CreateLimeobjectDialogCommand = __decorate([
    Command({
        id: 'limeobject.create-dialog',
    })
], CreateLimeobjectDialogCommand);

/**
 * Deletes the object from the database
 *
 * @id `limeobject.delete-object`
 * @public
 * @group Lime objects
 */
let DeleteObjectCommand = class DeleteObjectCommand {
};
DeleteObjectCommand = __decorate([
    Command({
        id: 'limeobject.delete-object',
    })
], DeleteObjectCommand);

/**
 * Open a dialog to view and edit object access information
 *
 * @id `limeobject.object-access`
 * @public
 * @group Lime objects
 */
let OpenObjectAccessDialogCommand = class OpenObjectAccessDialogCommand {
};
OpenObjectAccessDialogCommand = __decorate([
    Command({
        id: 'limeobject.object-access',
    })
], OpenObjectAccessDialogCommand);

/**
 * Saves the object to the database
 *
 * @id `limeobject.save-object`
 * @public
 * @group Lime objects
 */
let SaveLimeObjectCommand = class SaveLimeObjectCommand {
    constructor() {
        /**
         * Specifies if routing to limeobject should be done after confirmation
         */
        this.route = false;
    }
};
SaveLimeObjectCommand = __decorate([
    Command({
        id: 'limeobject.save-object',
    })
], SaveLimeObjectCommand);

/**
 * @public
 * @group Query
 */
var Operator;
(function (Operator) {
    Operator["AND"] = "AND";
    Operator["OR"] = "OR";
    Operator["NOT"] = "!";
    Operator["EQUALS"] = "=";
    Operator["NOT_EQUALS"] = "!=";
    Operator["GREATER"] = ">";
    Operator["LESS"] = "<";
    Operator["IN"] = "IN";
    Operator["BEGINS"] = "=?";
    Operator["LIKE"] = "?";
    Operator["LESS_OR_EQUAL"] = "<=";
    Operator["GREATER_OR_EQUAL"] = ">=";
    Operator["ENDS"] = "=$";
})(Operator || (Operator = {}));

const SERVICE_NAME$j = 'query';
PlatformServiceName.Query = SERVICE_NAME$j;

const SERVICE_NAME$i = 'http';
PlatformServiceName.Http = SERVICE_NAME$i;

const SERVICE_NAME$h = 'eventDispatcher';
PlatformServiceName.EventDispatcher = SERVICE_NAME$h;

const SERVICE_NAME$g = 'translate';
PlatformServiceName.Translate = SERVICE_NAME$g;

const SERVICE_NAME$f = 'dialog';
PlatformServiceName.Dialog = SERVICE_NAME$f;

const SERVICE_NAME$e = 'keybindingRegistry';
PlatformServiceName.KeybindingRegistry = SERVICE_NAME$e;

const SERVICE_NAME$d = 'navigator';
PlatformServiceName.Navigator = SERVICE_NAME$d;

/**
 * Navigates to a new location
 *
 * @id `navigator.navigate`
 * @beta
 * @group Navigation
 */
let NavigateCommand = class NavigateCommand {
};
NavigateCommand = __decorate([
    Command({
        id: 'navigator.navigate',
    })
], NavigateCommand);

const SERVICE_NAME$c = 'notifications';
PlatformServiceName.Notification = SERVICE_NAME$c;

const SERVICE_NAME$b = 'routeRegistry';
PlatformServiceName.RouteRegistry = SERVICE_NAME$b;

/**
 * @public
 * @group Tasks
 */
var TaskState;
(function (TaskState) {
    /**
     * Task state is unknown
     */
    TaskState["Pending"] = "PENDING";
    /**
     * Task was started by a worker
     */
    TaskState["Started"] = "STARTED";
    /**
     * Task is waiting for retry
     */
    TaskState["Retry"] = "RETRY";
    /**
     * Task succeeded
     */
    TaskState["Success"] = "SUCCESS";
    /**
     * Task failed
     */
    TaskState["Failure"] = "FAILURE";
})(TaskState || (TaskState = {}));
/**
 * Events dispatched by the task service
 * @public
 * @group Tasks
 */
var TaskEventType;
(function (TaskEventType) {
    /**
     * Dispatched when a task has been created.
     *
     * @see {@link TaskEvent}
     */
    TaskEventType["Created"] = "task.created";
    /**
     * Dispatched when the task has successfully been completed
     *
     * @see {@link TaskEvent}
     */
    TaskEventType["Success"] = "task.success";
    /**
     * Dispatched if an error occured while running the task
     *
     * @see {@link TaskEvent}
     */
    TaskEventType["Failed"] = "task.failed";
})(TaskEventType || (TaskEventType = {}));

const SERVICE_NAME$a = 'state.tasks';
PlatformServiceName.TaskRepository = SERVICE_NAME$a;

const SERVICE_NAME$9 = 'state.configs';
PlatformServiceName.ConfigRepository = SERVICE_NAME$9;

const SERVICE_NAME$8 = 'state.device';
PlatformServiceName.Device = SERVICE_NAME$8;

const SERVICE_NAME$7 = 'state.filters';
PlatformServiceName.FilterRepository = SERVICE_NAME$7;

const SERVICE_NAME$6 = 'state.user-data';
PlatformServiceName.UserDataRepository = SERVICE_NAME$6;

const SERVICE_NAME$5 = 'state.application';
PlatformServiceName.Application = SERVICE_NAME$5;

const SERVICE_NAME$4 = 'userPreferences';
PlatformServiceName.UserPreferencesRepository = SERVICE_NAME$4;

const SERVICE_NAME$3 = 'datetimeformatter';
PlatformServiceName.DateTimeFormatter = SERVICE_NAME$3;

const SERVICE_NAME$2 = 'conditionRegistry';
PlatformServiceName.ConditionRegistry = SERVICE_NAME$2;

const SERVICE_NAME$1 = 'viewFactoryRegistry';
PlatformServiceName.ViewFactoryRegistry = SERVICE_NAME$1;

const SERVICE_NAME = 'webComponentRegistry';
PlatformServiceName.WebComponentRegistry = SERVICE_NAME;

/* eslint-disable camelcase */
const fetchMe = async (platform, session) => {
    const options = {
        headers: getHeaders(session),
    };
    const { data } = await platform
        .get(PlatformServiceName.Http)
        .get('getaccept/me', options);
    return data;
};
const switchEntity = async (entity_id, platform, session) => {
    const options = {
        headers: getHeaders(session),
    };
    const payload = {
        entity_id: entity_id,
    };
    const { data } = await platform
        .get(PlatformServiceName.Http)
        .post('getaccept/switch-entity', payload, options);
    return data;
};
const fetchLimeDocuments = async (platform, limetype, record_id, selectedLimeDocument) => {
    const options = {
        params: {
            limetype: limetype,
            record_id: record_id.toString(),
        },
    };
    const documents = await platform
        .get(PlatformServiceName.Http)
        .get('getaccept/documents', options);
    return documents.map(document => ({
        text: document.comment ? document.comment : '(Empty description)',
        value: document.id,
        icon: {
            name: 'document',
            color: 'var(--lime-green)',
        },
        selected: selectedLimeDocument && selectedLimeDocument.value === document.id,
    }));
};
const fetchSentDocuments = async (platform, externalId, session) => {
    const options = {
        headers: {
            'ga-auth-token': session.access_token,
        },
        params: {
            external_id: externalId,
        },
    };
    const { documents } = await platform
        .get(PlatformServiceName.Http)
        .get('getaccept/sent-documents', options);
    return documents;
};
const fetchTemplates = async (platform, session, selectedTemplate) => {
    const options = {
        headers: {
            'ga-auth-token': session.access_token,
        },
    };
    const { templates = [] } = await platform
        .get(PlatformServiceName.Http)
        .get('getaccept/templates', options);
    return templates.map((template) => ({
        text: template.name,
        value: template.id,
        icon: 'document',
        iconColor: 'var(--lime-orange)',
        selected: selectedTemplate && selectedTemplate.value === template.id,
        thumbUrl: template.thumb_url,
    }));
};
const fetchTemplateFields = async (platform, session, limetype, record_id, selectedTemplate) => {
    const options = {
        headers: {
            'ga-auth-token': session.access_token,
        },
        params: {
            template_id: selectedTemplate.value,
            limetype: limetype,
            record_id: record_id.toString(),
        },
    };
    const { data: { fields = [] }, } = await platform
        .get(PlatformServiceName.Http)
        .get('getaccept/template-fields', options);
    return fields;
};
const fetchTemplateRoles = async (platform, session, limetype, record_id, selectedTemplate) => {
    const options = {
        headers: {
            'ga-auth-token': session.access_token,
        },
        params: {
            template_id: selectedTemplate.value,
            limetype: limetype,
            record_id: record_id.toString(),
        },
    };
    const { data } = await platform
        .get(PlatformServiceName.Http)
        .get('getaccept/template-roles', options);
    return (data === null || data === void 0 ? void 0 : data.roles) || [];
};
const fetchObjectProps = async (platform, session, limetype, record_id) => {
    const options = {
        headers: {
            'ga-auth-token': session.access_token,
        },
        params: {
            limetype: limetype,
            record_id: record_id.toString(),
        },
    };
    // eslint-disable-next-line no-return-await
    return await platform
        .get(PlatformServiceName.Http)
        .get('getaccept/object-props', options);
};
const fetchDealValue = async (platform, session, limetype, record_id) => {
    const options = {
        headers: {
            'ga-auth-token': session.access_token,
        },
        params: {
            limetype: limetype,
            record_id: record_id.toString(),
        },
    };
    // eslint-disable-next-line no-return-await
    return await platform
        .get(PlatformServiceName.Http)
        .get('getaccept/deal-value', options);
};
const getHeaders = (session) => {
    return {
        'ga-auth-token': session.access_token,
    };
};
const fetchEntity = async (platform, session) => {
    const options = {
        headers: getHeaders(session),
    };
    const { data } = await platform
        .get(PlatformServiceName.Http)
        .get('getaccept/entity', options);
    return data;
};
const fetchDocumentDetails = async (platform, session, document_id) => {
    const options = {
        headers: getHeaders(session),
        params: {
            document_id: document_id,
        },
    };
    const { data } = await platform
        .get(PlatformServiceName.Http)
        .get('getaccept/document-details', options);
    return data;
};
const fetchVideos = async (platform, session) => {
    const options = {
        headers: getHeaders(session),
    };
    const { data } = await platform
        .get(PlatformServiceName.Http)
        .get('getaccept/videos', options);
    return data;
};
const createDocument = async (platform, session, document) => {
    const options = {
        headers: getHeaders(session),
    };
    return platform
        .get(PlatformServiceName.Http)
        .post('getaccept/create-document', document, options);
};
const sealDocument = async (platform, session, documentId) => {
    const options = {
        headers: getHeaders(session),
    };
    const payload = {
        document_id: documentId,
    };
    return platform
        .get(PlatformServiceName.Http)
        .post('getaccept/seal-document', payload, options);
};
const uploadDocument = async (platform, session, documentId) => {
    const options = {
        headers: getHeaders(session),
    };
    const payload = {
        document_id: documentId,
    };
    return platform
        .get(PlatformServiceName.Http)
        .post('getaccept/upload-document', payload, options);
};
const removeDocument = async (platform, session, documentId) => {
    const options = {
        headers: getHeaders(session),
    };
    const payload = {
        document_id: documentId,
    };
    return platform
        .get(PlatformServiceName.Http)
        .post('getaccept/delete-document', payload, options);
};
const signup = async (platform, data) => {
    const payload = data;
    return platform
        .get(PlatformServiceName.Http)
        .post('getaccept/signup', payload);
};
const refreshToken = async (platform, session) => {
    const { access_token, expires_in } = session;
    return platform
        .get(PlatformServiceName.Http)
        .post('getaccept/refresh-token', {
        access_token: access_token,
        expires_in: expires_in,
    });
};

exports.PlatformServiceName = PlatformServiceName;
exports.createDocument = createDocument;
exports.fetchDealValue = fetchDealValue;
exports.fetchDocumentDetails = fetchDocumentDetails;
exports.fetchEntity = fetchEntity;
exports.fetchLimeDocuments = fetchLimeDocuments;
exports.fetchMe = fetchMe;
exports.fetchObjectProps = fetchObjectProps;
exports.fetchSentDocuments = fetchSentDocuments;
exports.fetchTemplateFields = fetchTemplateFields;
exports.fetchTemplateRoles = fetchTemplateRoles;
exports.fetchTemplates = fetchTemplates;
exports.fetchVideos = fetchVideos;
exports.refreshToken = refreshToken;
exports.removeDocument = removeDocument;
exports.sealDocument = sealDocument;
exports.signup = signup;
exports.switchEntity = switchEntity;
exports.uploadDocument = uploadDocument;

//# sourceMappingURL=index-30556617.js.map