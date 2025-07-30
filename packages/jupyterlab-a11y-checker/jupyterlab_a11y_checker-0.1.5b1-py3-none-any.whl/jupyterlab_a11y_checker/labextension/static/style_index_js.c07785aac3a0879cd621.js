"use strict";
(self["webpackChunkjupyterlab_a11y_checker"] = self["webpackChunkjupyterlab_a11y_checker"] || []).push([["style_index_js"],{

/***/ "./node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \**************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
___CSS_LOADER_EXPORT___.push([module.id, "@import url(https://fonts.googleapis.com/icon?family=Material+Icons);"]);
// Module
___CSS_LOADER_EXPORT___.push([module.id, `/* CSS Variables for Colors */
:root {
    /* These will be overridden by JupyterLab theme variables */
    --primary-blue: #2C5B8E;
    --primary-blue-hover: #2a4365;
    --text-light: var(--jp-ui-inverse-font-color1, #ffffff);
    --border-color: var(--jp-border-color1, #ddd);
    --error-red: var(--jp-error-color1, #DB3939);
    --success-green: var(--jp-success-color1, #28A745);
}

/* Import Material Icons */

/* ==========================================================================
   Main Panel Layout
   ========================================================================== */
.a11y-panel {
    background-color: var(--jp-layout-color1);
    height: 100%;
    overflow-y: auto;
}

.a11y-panel .main-container {
    padding: 0;
}

/* ==========================================================================
   Notice Section
   ========================================================================== */
.notice-container {
    background-color: var(--primary-blue);
    color: #ffffff;
    overflow: hidden;
    padding: 4px 8px;
}

.notice-container .chevron {
    color: #ffffff;
}

.notice-header {
    padding: 6px 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.notice-title {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #ffffff;
}

.triangle {
    font-size: 12px;
}

.notice-delete-button {
    background: none;
    border: none;
    color: #ffffff;
    cursor: pointer;
    font-size: 16px;
    padding: 4px;
}

.notice-content {
    padding: 8px 20px;
    color: #ffffff;
}

.notice-content a {
    color: #ffffff;
    text-decoration: underline;
}

/* ==========================================================================
   Main Title
   ========================================================================== */
.main-title {
    font-size: 24px;
    font-weight: bold;
    text-align: center;
    margin: 24px 4px;
    color: var(--jp-ui-font-color1);
}

/* ==========================================================================
   Controls Buttons Section
   ========================================================================== */
.controls-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    padding: 0 16px;
    margin-bottom: 24px;
}

.control-button {
    background-color: var(--primary-blue);
    color: #ffffff;
    border: none;
    border-radius: 4px;
    padding: 12px;
    font-size: 16px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    width: 60%;
}

.control-button svg {
    flex-shrink: 0;
    width: 24px;
    height: 24px;
    fill: #ffffff;
}

.control-button div {
    text-align: left;
    flex: 1;
    color: #ffffff;
}

.control-button:hover {
    background-color: var(--primary-blue-hover);
}

/* ==========================================================================
   Issue Categories Section
   ========================================================================== */
.issues-container {
    padding: 0 16px;
}

.no-issues {
    text-align: center;
    color: var(--jp-ui-font-color2);
    padding: 24px;
}

.category {
    margin-bottom: 24px;
}

.category-title {
    font-size: 20px;
    margin-bottom: 8px;
    color: var(--jp-ui-font-color1);
}

.category hr {
    border: none;
    border-top: 1px solid var(--border-color);
    margin: 0 0 16px 0;
}

.issues-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

/* ==========================================================================
   Issue Widget
   ========================================================================== */
.issue-widget {
    margin: 5px 0;
    margin-left: 12px;
}

.issue-widget .container {
    display: flex;
    flex-direction: column;
}

.issue-widget .issue-header-button {
    background: none;
    border: none;
    padding: 0;
    text-align: left;
    cursor: pointer;
    margin-bottom: 8px;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.issue-widget .issue-header {
    font-size: 16px;
    font-weight: 700;
    margin: 0;
    color: var(--jp-ui-font-color1);
    display: flex;
    align-items: center;
    gap: 4px;
}

.issue-widget .description {
    margin: 0 0 12px 0;
    font-size: 14px;
    color: var(--jp-ui-font-color1);
}

.issue-widget .detailed-description.visible {
    display: block;
}

.issue-widget .detailed-description {
    margin: 0 0 12px 0;
    font-size: 14px;
    display: none;
    color: var(--jp-ui-font-color1);
    transition: display 0.3s ease;
}

.issue-widget .detailed-description a {
    color: var(--jp-content-link-color);
    text-decoration: underline;
}

/* ==========================================================================
   Issue Widget Buttons Section
   ========================================================================== */
.issue-widget .button-container {
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
    gap: 12px;
    margin-bottom: 12px;
    width: 100%;
}

.issue-widget .button-container .jp-Button2 {
    flex: 1;
}

.jp-Button:hover,
.jp-Button2:hover {
    background-color: var(--primary-blue-hover);
}

/* Button-specific styles */
.jp-Button {
    min-width: 140px;
}

.jp-Button2 {
    background-color: #2c5282;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 7px 15px;
    cursor: pointer;
    font-size: 14px;
    gap: 4px;
    display: flex;
    flex-direction: row;
    align-items: center;
}

.apply-button,
.suggest-button {
    font-size: 12px;
    margin-left: auto;
    display: flex;
    width: auto !important;
}

.apply-button .material-icons,
.suggest-button .material-icons {
    font-size: 12px;
}

/* Suggestion Styles */
.issue-widget .suggestion-container {
    margin-bottom: 12px;
    margin-left: 30px;
    padding: 12px;
    border-radius: 4px;
    font-family: monospace;
}

.issue-widget .suggestion {
    word-wrap: break-word;
    white-space: pre-wrap;
}

.issue-widget .textfield-fix-widget {
    margin-bottom: 12px;
    padding: 6px;
    border-radius: 4px;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.textfield-fix-widget {
    padding: 12px;
    border-radius: 8px;
    margin-top: 12px;
    border: 1px solid var(--jp-border-color1);
    min-width: 145px;
}

.jp-a11y-input {
    width: calc(100% - 16px);
    padding: 8px;
    margin-bottom: 8px;
    font-family: Inter, sans-serif;
    border: none;
    outline: none;
    background-color: var(--jp-layout-color1);
    color: var(--jp-ui-font-color1);
}

.jp-a11y-input::placeholder {
    color: var(--jp-ui-font-color3);
}

.textfield-buttons {
    display: flex;
    justify-content: flex-end;
    flex-wrap: wrap;
    width: 100%;
}

.textfield-buttons .jp-Button2 {
    margin-left: 4px;
}

/* Collapsible Content */
.collapsible-content {
    padding-left: 20px;
    gap: 4px;
}

/* Icon Styles */
.icon {
    width: 18px;
    height: 18px;
    fill: currentColor;
}

.chevron {
    transition: transform 0.3s ease;
    transform-origin: center center;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    line-height: 1;
    color: var(--jp-ui-font-color1);
}

.chevron.expanded {
    transform: rotate(180deg);
}

.loading {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

/* Material Icons Styles */
.material-icons {
    font-family: 'Material Icons';
    font-weight: normal;
    font-style: normal;
    font-size: 24px;
    /* Preferred icon size */
    display: inline-block;
    line-height: 1;
    text-transform: none;
    letter-spacing: normal;
    word-wrap: normal;
    white-space: nowrap;
    direction: ltr;
    vertical-align: middle;
}

/* Icon sizes */
.material-icons.md-18 {
    font-size: 18px;
}

.material-icons.md-24 {
    font-size: 24px;
}

.material-icons.md-36 {
    font-size: 36px;
}

.material-icons.md-48 {
    font-size: 48px;
}

/* Icon colors */
.material-icons.md-dark {
    color: rgba(0, 0, 0, 0.54);
}

.material-icons.md-dark.md-inactive {
    color: rgba(0, 0, 0, 0.26);
}

.material-icons.md-light {
    color: rgba(255, 255, 255, 1);
}

.material-icons.md-light.md-inactive {
    color: rgba(255, 255, 255, 0.3);
}

/* Loading animation for Material Icons */
.material-icons.loading {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

.hidden:not(.dropdown-content) {
    display: none;
}

.table-header-fix-widget {
    margin-top: 8px;
}

.table-header-fix-widget .button-container {
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
    gap: 8px;
}

.custom-dropdown {
    position: relative;
    width: calc(100% - 16px);
    margin-bottom: 8px;
    z-index: 9999;
    isolation: isolate;
}

.dropdown-button {
    width: 100%;
    padding: 8px 12px;
    background-color: var(--jp-layout-color1);
    color: var(--jp-ui-font-color1);
    border: 1px solid var(--jp-border-color1);
    border-radius: 4px;
    cursor: pointer;
    font-family: var(--jp-ui-font-family);
    font-size: 14px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.dropdown-button:hover,
.dropdown-button.active {
    background-color: var(--primary-blue-hover);
    color: var(--text-light);
}

.dropdown-text {
    flex: 1;
    text-align: left;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.dropdown-arrow {
    margin-left: 8px;
    flex-shrink: 0;
}

.dropdown-content {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background-color: var(--jp-layout-color1);
    border: 1px solid var(--jp-border-color1);
    border-radius: 4px;
    margin-top: 4px;
    z-index: 1000;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.dropdown-content.hidden {
    display: none;
}

.dropdown-option {
    padding: 8px 12px;
    cursor: pointer;
    color: var(--jp-ui-font-color1);
}

.dropdown-option:hover {
    background-color: var(--primary-blue-hover);
    color: #ffffff;
}

/* ==========================================================================
   Material Icons
   ========================================================================== */
.material-icons {
    font-family: 'Material Icons';
    font-weight: normal;
    font-style: normal;
    font-size: 24px;
    display: inline-block;
    line-height: 1;
    text-transform: none;
    letter-spacing: normal;
    word-wrap: normal;
    white-space: nowrap;
    direction: ltr;
    vertical-align: middle;
}

/* Icon sizes */
.material-icons.md-18 {
    font-size: 18px;
}

.material-icons.md-24 {
    font-size: 24px;
}

.material-icons.md-36 {
    font-size: 36px;
}

.material-icons.md-48 {
    font-size: 48px;
}

/* Icon colors */
.material-icons.md-dark {
    color: var(--jp-ui-font-color1);
}

.material-icons.md-dark.md-inactive {
    color: var(--jp-ui-font-color3);
}

.material-icons.md-light {
    color: var(--jp-ui-inverse-font-color1);
}

.material-icons.md-light.md-inactive {
    color: var(--jp-ui-inverse-font-color3);
}

/* ==========================================================================
   Animations
   ========================================================================== */
.loading {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

/* ==========================================================================
   Utility Classes
   ========================================================================== */
.hidden:not(.dropdown-content) {
    display: none;
}

/* ==========================================================================
   Fix Widgets
   ========================================================================== */
.table-header-fix-widget {
    margin-top: 8px;
}

.table-header-fix-widget .button-container {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
}

.fix-description {
    margin-bottom: 8px;
    line-height: 1.4;
    color: var(--jp-ui-font-color1);
}

.dropdown-fix-widget .fix-description {
    margin-bottom: 12px;
}

.loading-overlay {
    position: absolute;
    left: 8px;
    top: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.loading-overlay .material-icons.loading {
    animation: spin 1s linear infinite;
}`, "",{"version":3,"sources":["webpack://./style/base.css"],"names":[],"mappings":"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","sourcesContent":["/* CSS Variables for Colors */\n:root {\n    /* These will be overridden by JupyterLab theme variables */\n    --primary-blue: #2C5B8E;\n    --primary-blue-hover: #2a4365;\n    --text-light: var(--jp-ui-inverse-font-color1, #ffffff);\n    --border-color: var(--jp-border-color1, #ddd);\n    --error-red: var(--jp-error-color1, #DB3939);\n    --success-green: var(--jp-success-color1, #28A745);\n}\n\n/* Import Material Icons */\n@import url('https://fonts.googleapis.com/icon?family=Material+Icons');\n\n/* ==========================================================================\n   Main Panel Layout\n   ========================================================================== */\n.a11y-panel {\n    background-color: var(--jp-layout-color1);\n    height: 100%;\n    overflow-y: auto;\n}\n\n.a11y-panel .main-container {\n    padding: 0;\n}\n\n/* ==========================================================================\n   Notice Section\n   ========================================================================== */\n.notice-container {\n    background-color: var(--primary-blue);\n    color: #ffffff;\n    overflow: hidden;\n    padding: 4px 8px;\n}\n\n.notice-container .chevron {\n    color: #ffffff;\n}\n\n.notice-header {\n    padding: 6px 8px;\n    display: flex;\n    justify-content: space-between;\n    align-items: center;\n}\n\n.notice-title {\n    display: flex;\n    align-items: center;\n    gap: 8px;\n    color: #ffffff;\n}\n\n.triangle {\n    font-size: 12px;\n}\n\n.notice-delete-button {\n    background: none;\n    border: none;\n    color: #ffffff;\n    cursor: pointer;\n    font-size: 16px;\n    padding: 4px;\n}\n\n.notice-content {\n    padding: 8px 20px;\n    color: #ffffff;\n}\n\n.notice-content a {\n    color: #ffffff;\n    text-decoration: underline;\n}\n\n/* ==========================================================================\n   Main Title\n   ========================================================================== */\n.main-title {\n    font-size: 24px;\n    font-weight: bold;\n    text-align: center;\n    margin: 24px 4px;\n    color: var(--jp-ui-font-color1);\n}\n\n/* ==========================================================================\n   Controls Buttons Section\n   ========================================================================== */\n.controls-container {\n    display: flex;\n    flex-direction: column;\n    align-items: center;\n    gap: 12px;\n    padding: 0 16px;\n    margin-bottom: 24px;\n}\n\n.control-button {\n    background-color: var(--primary-blue);\n    color: #ffffff;\n    border: none;\n    border-radius: 4px;\n    padding: 12px;\n    font-size: 16px;\n    cursor: pointer;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    gap: 8px;\n    width: 60%;\n}\n\n.control-button svg {\n    flex-shrink: 0;\n    width: 24px;\n    height: 24px;\n    fill: #ffffff;\n}\n\n.control-button div {\n    text-align: left;\n    flex: 1;\n    color: #ffffff;\n}\n\n.control-button:hover {\n    background-color: var(--primary-blue-hover);\n}\n\n/* ==========================================================================\n   Issue Categories Section\n   ========================================================================== */\n.issues-container {\n    padding: 0 16px;\n}\n\n.no-issues {\n    text-align: center;\n    color: var(--jp-ui-font-color2);\n    padding: 24px;\n}\n\n.category {\n    margin-bottom: 24px;\n}\n\n.category-title {\n    font-size: 20px;\n    margin-bottom: 8px;\n    color: var(--jp-ui-font-color1);\n}\n\n.category hr {\n    border: none;\n    border-top: 1px solid var(--border-color);\n    margin: 0 0 16px 0;\n}\n\n.issues-list {\n    display: flex;\n    flex-direction: column;\n    gap: 12px;\n}\n\n/* ==========================================================================\n   Issue Widget\n   ========================================================================== */\n.issue-widget {\n    margin: 5px 0;\n    margin-left: 12px;\n}\n\n.issue-widget .container {\n    display: flex;\n    flex-direction: column;\n}\n\n.issue-widget .issue-header-button {\n    background: none;\n    border: none;\n    padding: 0;\n    text-align: left;\n    cursor: pointer;\n    margin-bottom: 8px;\n    width: 100%;\n    display: flex;\n    justify-content: space-between;\n    align-items: center;\n}\n\n.issue-widget .issue-header {\n    font-size: 16px;\n    font-weight: 700;\n    margin: 0;\n    color: var(--jp-ui-font-color1);\n    display: flex;\n    align-items: center;\n    gap: 4px;\n}\n\n.issue-widget .description {\n    margin: 0 0 12px 0;\n    font-size: 14px;\n    color: var(--jp-ui-font-color1);\n}\n\n.issue-widget .detailed-description.visible {\n    display: block;\n}\n\n.issue-widget .detailed-description {\n    margin: 0 0 12px 0;\n    font-size: 14px;\n    display: none;\n    color: var(--jp-ui-font-color1);\n    transition: display 0.3s ease;\n}\n\n.issue-widget .detailed-description a {\n    color: var(--jp-content-link-color);\n    text-decoration: underline;\n}\n\n/* ==========================================================================\n   Issue Widget Buttons Section\n   ========================================================================== */\n.issue-widget .button-container {\n    display: flex;\n    flex-direction: row;\n    justify-content: flex-end;\n    gap: 12px;\n    margin-bottom: 12px;\n    width: 100%;\n}\n\n.issue-widget .button-container .jp-Button2 {\n    flex: 1;\n}\n\n.jp-Button:hover,\n.jp-Button2:hover {\n    background-color: var(--primary-blue-hover);\n}\n\n/* Button-specific styles */\n.jp-Button {\n    min-width: 140px;\n}\n\n.jp-Button2 {\n    background-color: #2c5282;\n    color: white;\n    border: none;\n    border-radius: 4px;\n    padding: 7px 15px;\n    cursor: pointer;\n    font-size: 14px;\n    gap: 4px;\n    display: flex;\n    flex-direction: row;\n    align-items: center;\n}\n\n.apply-button,\n.suggest-button {\n    font-size: 12px;\n    margin-left: auto;\n    display: flex;\n    width: auto !important;\n}\n\n.apply-button .material-icons,\n.suggest-button .material-icons {\n    font-size: 12px;\n}\n\n/* Suggestion Styles */\n.issue-widget .suggestion-container {\n    margin-bottom: 12px;\n    margin-left: 30px;\n    padding: 12px;\n    border-radius: 4px;\n    font-family: monospace;\n}\n\n.issue-widget .suggestion {\n    word-wrap: break-word;\n    white-space: pre-wrap;\n}\n\n.issue-widget .textfield-fix-widget {\n    margin-bottom: 12px;\n    padding: 6px;\n    border-radius: 4px;\n    display: flex;\n    flex-direction: column;\n    gap: 4px;\n}\n\n.textfield-fix-widget {\n    padding: 12px;\n    border-radius: 8px;\n    margin-top: 12px;\n    border: 1px solid var(--jp-border-color1);\n    min-width: 145px;\n}\n\n.jp-a11y-input {\n    width: calc(100% - 16px);\n    padding: 8px;\n    margin-bottom: 8px;\n    font-family: Inter, sans-serif;\n    border: none;\n    outline: none;\n    background-color: var(--jp-layout-color1);\n    color: var(--jp-ui-font-color1);\n}\n\n.jp-a11y-input::placeholder {\n    color: var(--jp-ui-font-color3);\n}\n\n.textfield-buttons {\n    display: flex;\n    justify-content: flex-end;\n    flex-wrap: wrap;\n    width: 100%;\n}\n\n.textfield-buttons .jp-Button2 {\n    margin-left: 4px;\n}\n\n/* Collapsible Content */\n.collapsible-content {\n    padding-left: 20px;\n    gap: 4px;\n}\n\n/* Icon Styles */\n.icon {\n    width: 18px;\n    height: 18px;\n    fill: currentColor;\n}\n\n.chevron {\n    transition: transform 0.3s ease;\n    transform-origin: center center;\n    display: inline-flex;\n    align-items: center;\n    justify-content: center;\n    width: 24px;\n    height: 24px;\n    line-height: 1;\n    color: var(--jp-ui-font-color1);\n}\n\n.chevron.expanded {\n    transform: rotate(180deg);\n}\n\n.loading {\n    animation: spin 1s linear infinite;\n}\n\n@keyframes spin {\n    0% {\n        transform: rotate(0deg);\n    }\n\n    100% {\n        transform: rotate(360deg);\n    }\n}\n\n/* Material Icons Styles */\n.material-icons {\n    font-family: 'Material Icons';\n    font-weight: normal;\n    font-style: normal;\n    font-size: 24px;\n    /* Preferred icon size */\n    display: inline-block;\n    line-height: 1;\n    text-transform: none;\n    letter-spacing: normal;\n    word-wrap: normal;\n    white-space: nowrap;\n    direction: ltr;\n    vertical-align: middle;\n}\n\n/* Icon sizes */\n.material-icons.md-18 {\n    font-size: 18px;\n}\n\n.material-icons.md-24 {\n    font-size: 24px;\n}\n\n.material-icons.md-36 {\n    font-size: 36px;\n}\n\n.material-icons.md-48 {\n    font-size: 48px;\n}\n\n/* Icon colors */\n.material-icons.md-dark {\n    color: rgba(0, 0, 0, 0.54);\n}\n\n.material-icons.md-dark.md-inactive {\n    color: rgba(0, 0, 0, 0.26);\n}\n\n.material-icons.md-light {\n    color: rgba(255, 255, 255, 1);\n}\n\n.material-icons.md-light.md-inactive {\n    color: rgba(255, 255, 255, 0.3);\n}\n\n/* Loading animation for Material Icons */\n.material-icons.loading {\n    animation: spin 1s linear infinite;\n}\n\n@keyframes spin {\n    0% {\n        transform: rotate(0deg);\n    }\n\n    100% {\n        transform: rotate(360deg);\n    }\n}\n\n.hidden:not(.dropdown-content) {\n    display: none;\n}\n\n.table-header-fix-widget {\n    margin-top: 8px;\n}\n\n.table-header-fix-widget .button-container {\n    display: flex;\n    flex-direction: row;\n    justify-content: flex-end;\n    gap: 8px;\n}\n\n.custom-dropdown {\n    position: relative;\n    width: calc(100% - 16px);\n    margin-bottom: 8px;\n    z-index: 9999;\n    isolation: isolate;\n}\n\n.dropdown-button {\n    width: 100%;\n    padding: 8px 12px;\n    background-color: var(--jp-layout-color1);\n    color: var(--jp-ui-font-color1);\n    border: 1px solid var(--jp-border-color1);\n    border-radius: 4px;\n    cursor: pointer;\n    font-family: var(--jp-ui-font-family);\n    font-size: 14px;\n    height: 40px;\n    display: flex;\n    align-items: center;\n    justify-content: space-between;\n}\n\n.dropdown-button:hover,\n.dropdown-button.active {\n    background-color: var(--primary-blue-hover);\n    color: var(--text-light);\n}\n\n.dropdown-text {\n    flex: 1;\n    text-align: left;\n    white-space: nowrap;\n    overflow: hidden;\n    text-overflow: ellipsis;\n}\n\n.dropdown-arrow {\n    margin-left: 8px;\n    flex-shrink: 0;\n}\n\n.dropdown-content {\n    position: absolute;\n    top: 100%;\n    left: 0;\n    right: 0;\n    background-color: var(--jp-layout-color1);\n    border: 1px solid var(--jp-border-color1);\n    border-radius: 4px;\n    margin-top: 4px;\n    z-index: 1000;\n    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);\n}\n\n.dropdown-content.hidden {\n    display: none;\n}\n\n.dropdown-option {\n    padding: 8px 12px;\n    cursor: pointer;\n    color: var(--jp-ui-font-color1);\n}\n\n.dropdown-option:hover {\n    background-color: var(--primary-blue-hover);\n    color: #ffffff;\n}\n\n/* ==========================================================================\n   Material Icons\n   ========================================================================== */\n.material-icons {\n    font-family: 'Material Icons';\n    font-weight: normal;\n    font-style: normal;\n    font-size: 24px;\n    display: inline-block;\n    line-height: 1;\n    text-transform: none;\n    letter-spacing: normal;\n    word-wrap: normal;\n    white-space: nowrap;\n    direction: ltr;\n    vertical-align: middle;\n}\n\n/* Icon sizes */\n.material-icons.md-18 {\n    font-size: 18px;\n}\n\n.material-icons.md-24 {\n    font-size: 24px;\n}\n\n.material-icons.md-36 {\n    font-size: 36px;\n}\n\n.material-icons.md-48 {\n    font-size: 48px;\n}\n\n/* Icon colors */\n.material-icons.md-dark {\n    color: var(--jp-ui-font-color1);\n}\n\n.material-icons.md-dark.md-inactive {\n    color: var(--jp-ui-font-color3);\n}\n\n.material-icons.md-light {\n    color: var(--jp-ui-inverse-font-color1);\n}\n\n.material-icons.md-light.md-inactive {\n    color: var(--jp-ui-inverse-font-color3);\n}\n\n/* ==========================================================================\n   Animations\n   ========================================================================== */\n.loading {\n    animation: spin 1s linear infinite;\n}\n\n@keyframes spin {\n    0% {\n        transform: rotate(0deg);\n    }\n\n    100% {\n        transform: rotate(360deg);\n    }\n}\n\n/* ==========================================================================\n   Utility Classes\n   ========================================================================== */\n.hidden:not(.dropdown-content) {\n    display: none;\n}\n\n/* ==========================================================================\n   Fix Widgets\n   ========================================================================== */\n.table-header-fix-widget {\n    margin-top: 8px;\n}\n\n.table-header-fix-widget .button-container {\n    display: flex;\n    justify-content: flex-end;\n    gap: 8px;\n}\n\n.fix-description {\n    margin-bottom: 8px;\n    line-height: 1.4;\n    color: var(--jp-ui-font-color1);\n}\n\n.dropdown-fix-widget .fix-description {\n    margin-bottom: 12px;\n}\n\n.loading-overlay {\n    position: absolute;\n    left: 8px;\n    top: 8px;\n    display: flex;\n    align-items: center;\n    gap: 8px;\n}\n\n.loading-overlay .material-icons.loading {\n    animation: spin 1s linear infinite;\n}"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {



/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
module.exports = function (cssWithMappingToString) {
  var list = [];

  // return the list of modules as css string
  list.toString = function toString() {
    return this.map(function (item) {
      var content = "";
      var needLayer = typeof item[5] !== "undefined";
      if (item[4]) {
        content += "@supports (".concat(item[4], ") {");
      }
      if (item[2]) {
        content += "@media ".concat(item[2], " {");
      }
      if (needLayer) {
        content += "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {");
      }
      content += cssWithMappingToString(item);
      if (needLayer) {
        content += "}";
      }
      if (item[2]) {
        content += "}";
      }
      if (item[4]) {
        content += "}";
      }
      return content;
    }).join("");
  };

  // import a list of modules into the list
  list.i = function i(modules, media, dedupe, supports, layer) {
    if (typeof modules === "string") {
      modules = [[null, modules, undefined]];
    }
    var alreadyImportedModules = {};
    if (dedupe) {
      for (var k = 0; k < this.length; k++) {
        var id = this[k][0];
        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }
    for (var _k = 0; _k < modules.length; _k++) {
      var item = [].concat(modules[_k]);
      if (dedupe && alreadyImportedModules[item[0]]) {
        continue;
      }
      if (typeof layer !== "undefined") {
        if (typeof item[5] === "undefined") {
          item[5] = layer;
        } else {
          item[1] = "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {").concat(item[1], "}");
          item[5] = layer;
        }
      }
      if (media) {
        if (!item[2]) {
          item[2] = media;
        } else {
          item[1] = "@media ".concat(item[2], " {").concat(item[1], "}");
          item[2] = media;
        }
      }
      if (supports) {
        if (!item[4]) {
          item[4] = "".concat(supports);
        } else {
          item[1] = "@supports (".concat(item[4], ") {").concat(item[1], "}");
          item[4] = supports;
        }
      }
      list.push(item);
    }
  };
  return list;
};

/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/sourceMaps.js":
/*!************************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/sourceMaps.js ***!
  \************************************************************/
/***/ ((module) => {



module.exports = function (item) {
  var content = item[1];
  var cssMapping = item[3];
  if (!cssMapping) {
    return content;
  }
  if (typeof btoa === "function") {
    var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(cssMapping))));
    var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
    var sourceMapping = "/*# ".concat(data, " */");
    return [content].concat([sourceMapping]).join("\n");
  }
  return [content].join("\n");
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module) => {



var stylesInDOM = [];
function getIndexByIdentifier(identifier) {
  var result = -1;
  for (var i = 0; i < stylesInDOM.length; i++) {
    if (stylesInDOM[i].identifier === identifier) {
      result = i;
      break;
    }
  }
  return result;
}
function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];
  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var indexByIdentifier = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3],
      supports: item[4],
      layer: item[5]
    };
    if (indexByIdentifier !== -1) {
      stylesInDOM[indexByIdentifier].references++;
      stylesInDOM[indexByIdentifier].updater(obj);
    } else {
      var updater = addElementStyle(obj, options);
      options.byIndex = i;
      stylesInDOM.splice(i, 0, {
        identifier: identifier,
        updater: updater,
        references: 1
      });
    }
    identifiers.push(identifier);
  }
  return identifiers;
}
function addElementStyle(obj, options) {
  var api = options.domAPI(options);
  api.update(obj);
  var updater = function updater(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap && newObj.supports === obj.supports && newObj.layer === obj.layer) {
        return;
      }
      api.update(obj = newObj);
    } else {
      api.remove();
    }
  };
  return updater;
}
module.exports = function (list, options) {
  options = options || {};
  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];
    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDOM[index].references--;
    }
    var newLastIdentifiers = modulesToDom(newList, options);
    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];
      var _index = getIndexByIdentifier(_identifier);
      if (stylesInDOM[_index].references === 0) {
        stylesInDOM[_index].updater();
        stylesInDOM.splice(_index, 1);
      }
    }
    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertBySelector.js":
/*!********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertBySelector.js ***!
  \********************************************************************/
/***/ ((module) => {



var memo = {};

/* istanbul ignore next  */
function getTarget(target) {
  if (typeof memo[target] === "undefined") {
    var styleTarget = document.querySelector(target);

    // Special case to return head of iframe instead of iframe itself
    if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
      try {
        // This will throw an exception if access to iframe is blocked
        // due to cross-origin restrictions
        styleTarget = styleTarget.contentDocument.head;
      } catch (e) {
        // istanbul ignore next
        styleTarget = null;
      }
    }
    memo[target] = styleTarget;
  }
  return memo[target];
}

/* istanbul ignore next  */
function insertBySelector(insert, style) {
  var target = getTarget(insert);
  if (!target) {
    throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
  }
  target.appendChild(style);
}
module.exports = insertBySelector;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertStyleElement.js":
/*!**********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertStyleElement.js ***!
  \**********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function insertStyleElement(options) {
  var element = document.createElement("style");
  options.setAttributes(element, options.attributes);
  options.insert(element, options.options);
  return element;
}
module.exports = insertStyleElement;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js":
/*!**********************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js ***!
  \**********************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {



/* istanbul ignore next  */
function setAttributesWithoutAttributes(styleElement) {
  var nonce =  true ? __webpack_require__.nc : 0;
  if (nonce) {
    styleElement.setAttribute("nonce", nonce);
  }
}
module.exports = setAttributesWithoutAttributes;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleDomAPI.js":
/*!***************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleDomAPI.js ***!
  \***************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function apply(styleElement, options, obj) {
  var css = "";
  if (obj.supports) {
    css += "@supports (".concat(obj.supports, ") {");
  }
  if (obj.media) {
    css += "@media ".concat(obj.media, " {");
  }
  var needLayer = typeof obj.layer !== "undefined";
  if (needLayer) {
    css += "@layer".concat(obj.layer.length > 0 ? " ".concat(obj.layer) : "", " {");
  }
  css += obj.css;
  if (needLayer) {
    css += "}";
  }
  if (obj.media) {
    css += "}";
  }
  if (obj.supports) {
    css += "}";
  }
  var sourceMap = obj.sourceMap;
  if (sourceMap && typeof btoa !== "undefined") {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  }

  // For old IE
  /* istanbul ignore if  */
  options.styleTagTransform(css, styleElement, options.options);
}
function removeStyleElement(styleElement) {
  // istanbul ignore if
  if (styleElement.parentNode === null) {
    return false;
  }
  styleElement.parentNode.removeChild(styleElement);
}

/* istanbul ignore next  */
function domAPI(options) {
  if (typeof document === "undefined") {
    return {
      update: function update() {},
      remove: function remove() {}
    };
  }
  var styleElement = options.insertStyleElement(options);
  return {
    update: function update(obj) {
      apply(styleElement, options, obj);
    },
    remove: function remove() {
      removeStyleElement(styleElement);
    }
  };
}
module.exports = domAPI;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleTagTransform.js":
/*!*********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleTagTransform.js ***!
  \*********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function styleTagTransform(css, styleElement) {
  if (styleElement.styleSheet) {
    styleElement.styleSheet.cssText = css;
  } else {
    while (styleElement.firstChild) {
      styleElement.removeChild(styleElement.firstChild);
    }
    styleElement.appendChild(document.createTextNode(css));
  }
}
module.exports = styleTagTransform;

/***/ }),

/***/ "./style/base.css":
/*!************************!*\
  !*** ./style/base.css ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./base.css */ "./node_modules/css-loader/dist/cjs.js!./style/base.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./style/index.js":
/*!************************!*\
  !*** ./style/index.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./base.css */ "./style/base.css");



/***/ })

}]);
//# sourceMappingURL=style_index_js.c07785aac3a0879cd621.js.map