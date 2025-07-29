"use strict";
(self["webpackChunkegi_jupyterlab_ext"] = self["webpackChunkegi_jupyterlab_ext"] || []).push([["lib_index_js"],{

/***/ "./lib/components/AddButton.js":
/*!*************************************!*\
  !*** ./lib/components/AddButton.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ AddButton)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _mui_icons_material_AddCircleOutlineRounded__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/icons-material/AddCircleOutlineRounded */ "./node_modules/@mui/icons-material/esm/AddCircleOutlineRounded.js");



function AddButton({ handleClickButton }) {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Button, { onClick: handleClickButton, size: "small", startIcon: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_AddCircleOutlineRounded__WEBPACK_IMPORTED_MODULE_2__["default"], null), sx: { textTransform: 'none' } }, "Add chart"));
}


/***/ }),

/***/ "./lib/components/ChartWrapper.js":
/*!****************************************!*\
  !*** ./lib/components/ChartWrapper.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ ChartWrapper)
/* harmony export */ });
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _NumberInput__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./NumberInput */ "./lib/components/NumberInput.js");
/* harmony import */ var _RefreshButton__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./RefreshButton */ "./lib/components/RefreshButton.js");
/* harmony import */ var _DeleteIconButton__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./DeleteIconButton */ "./lib/components/DeleteIconButton.js");
/* harmony import */ var _helpers_constants__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../helpers/constants */ "./lib/helpers/constants.js");






function debounce(func, delay) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => func(...args), delay);
    };
}
function ChartWrapper({ keyId, src, width, height, onDelete }) {
    const iframeRef = react__WEBPACK_IMPORTED_MODULE_1___default().useRef(null);
    const [refreshRateS, setRefreshRateS] = react__WEBPACK_IMPORTED_MODULE_1___default().useState(_helpers_constants__WEBPACK_IMPORTED_MODULE_2__.DEFAULT_REFRESH_RATE);
    const initialSrcWithRefresh = `${src}&refresh=${refreshRateS}s`;
    const [iframeSrc, setIframeSrc] = react__WEBPACK_IMPORTED_MODULE_1___default().useState(initialSrcWithRefresh);
    function refreshUrl() {
        setIframeSrc(prevState => {
            const base = prevState.split('&refresh=')[0];
            return `${base}&refresh=${refreshRateS}s`;
        });
    }
    react__WEBPACK_IMPORTED_MODULE_1___default().useEffect(() => {
        refreshUrl();
        const intervalId = setInterval(() => {
            refreshUrl();
        }, refreshRateS * 1000);
        // Whenever the refresh interval is cleared.
        return () => clearInterval(intervalId);
    }, [refreshRateS]);
    function handleRefreshClick() {
        if (iframeRef.current) {
            const copy_src = structuredClone(iframeRef.current.src);
            iframeRef.current.src = copy_src;
        }
    }
    // Call the debounced function on number change
    function handleNumberChange(value) {
        const parsedValue = Number(value);
        if (!isNaN(parsedValue)) {
            debouncedSetRefreshRateS(parsedValue);
        }
    }
    // Create a debounced version of setRefreshRateS
    // Using 200ms delay instead of 2ms for a noticeable debounce effect.
    const debouncedSetRefreshRateS = react__WEBPACK_IMPORTED_MODULE_1___default().useMemo(() => debounce((value) => setRefreshRateS(value), 1000), []);
    return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react__WEBPACK_IMPORTED_MODULE_1___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("iframe", { src: iframeSrc, width: width, height: height, sandbox: "allow-scripts allow-same-origin", ref: iframeRef, id: `iframe-item-${keyId}` }),
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_0__.Grid2, null,
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_RefreshButton__WEBPACK_IMPORTED_MODULE_3__["default"], { handleRefreshClick: handleRefreshClick }),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_NumberInput__WEBPACK_IMPORTED_MODULE_4__["default"]
            // currentRefreshValue={refreshRateS}
            , { 
                // currentRefreshValue={refreshRateS}
                handleRefreshNumberChange: newValue => handleNumberChange(newValue) }),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_DeleteIconButton__WEBPACK_IMPORTED_MODULE_5__["default"], { handleClickButton: () => onDelete(keyId) }))));
}


/***/ }),

/***/ "./lib/components/DeleteIconButton.js":
/*!********************************************!*\
  !*** ./lib/components/DeleteIconButton.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ DeleteIconButton)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _mui_icons_material_DeleteOutlineRounded__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/icons-material/DeleteOutlineRounded */ "./node_modules/@mui/icons-material/esm/DeleteOutlineRounded.js");



function DeleteIconButton({ handleClickButton }) {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.IconButton, { onClick: handleClickButton, size: "small" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_DeleteOutlineRounded__WEBPACK_IMPORTED_MODULE_2__["default"], null)));
}


/***/ }),

/***/ "./lib/components/GoBackButton.js":
/*!****************************************!*\
  !*** ./lib/components/GoBackButton.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ GoBackButton)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _mui_icons_material_ArrowBackRounded__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/icons-material/ArrowBackRounded */ "./node_modules/@mui/icons-material/esm/ArrowBackRounded.js");



function GoBackButton({ handleClick }) {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.IconButton, { onClick: handleClick, size: "small" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_ArrowBackRounded__WEBPACK_IMPORTED_MODULE_2__["default"], null)));
}


/***/ }),

/***/ "./lib/components/NumberInput.js":
/*!***************************************!*\
  !*** ./lib/components/NumberInput.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ NumberInput)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _helpers_constants__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../helpers/constants */ "./lib/helpers/constants.js");



function NumberInput({ 
// currentRefreshValue,
handleRefreshNumberChange }) {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.TextField, { id: "outlined-number", label: "Refresh(S)", type: "number", slotProps: {
            inputLabel: {
                shrink: true
            }
        }, onChange: event => handleRefreshNumberChange(event.target.value), defaultValue: _helpers_constants__WEBPACK_IMPORTED_MODULE_2__.DEFAULT_REFRESH_RATE, size: "small", sx: { maxWidth: 90 } }));
}


/***/ }),

/***/ "./lib/components/RefreshButton.js":
/*!*****************************************!*\
  !*** ./lib/components/RefreshButton.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ RefreshButton)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _mui_icons_material_RefreshRounded__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/icons-material/RefreshRounded */ "./node_modules/@mui/icons-material/esm/RefreshRounded.js");



function RefreshButton({ handleRefreshClick }) {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.IconButton, { onClick: handleRefreshClick, size: "small" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_RefreshRounded__WEBPACK_IMPORTED_MODULE_2__["default"], null))));
}


/***/ }),

/***/ "./lib/components/SelectComponent.js":
/*!*******************************************!*\
  !*** ./lib/components/SelectComponent.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ MultipleSelectCheckmarks)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material_OutlinedInput__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @mui/material/OutlinedInput */ "./node_modules/@mui/material/OutlinedInput/OutlinedInput.js");
/* harmony import */ var _mui_material_MenuItem__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @mui/material/MenuItem */ "./node_modules/@mui/material/MenuItem/MenuItem.js");
/* harmony import */ var _mui_material_FormControl__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material/FormControl */ "./node_modules/@mui/material/FormControl/FormControl.js");
/* harmony import */ var _mui_material_ListItemText__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @mui/material/ListItemText */ "./node_modules/@mui/material/ListItemText/ListItemText.js");
/* harmony import */ var _mui_material_Select__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material/Select */ "./node_modules/@mui/material/Select/Select.js");
/* harmony import */ var _mui_material_Checkbox__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @mui/material/Checkbox */ "./node_modules/@mui/material/Checkbox/Checkbox.js");
/* harmony import */ var _helpers_constants__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../helpers/constants */ "./lib/helpers/constants.js");








const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
    PaperProps: {
        style: {
            maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
            width: 250
        }
    }
};
const metrics = [
    'CPU Usage',
    'CPU Time',
    'CPU Frequency',
    'Memory Energy',
    'Memory Used',
    'Network I/O',
    'Network Connections'
];
const noMetricSelected = 'No metric selected';
function MultipleSelectCheckmarks() {
    const [metricName, setMetricName] = react__WEBPACK_IMPORTED_MODULE_0__.useState([]);
    const handleChange = (event) => {
        const { target: { value } } = event;
        setMetricName(
        // On autofill we get a stringified value.
        typeof value === 'string' ? value.split(',') : value);
    };
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null,
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_FormControl__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: { width: '100%' } },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Select__WEBPACK_IMPORTED_MODULE_2__["default"], { labelId: "metrics-multiple-checkbox-label", id: "metrics-multiple-checkbox", multiple: true, value: metricName, onChange: handleChange, input: react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_OutlinedInput__WEBPACK_IMPORTED_MODULE_3__["default"], { label: "Metric", sx: { width: '100%' } }), renderValue: selected => {
                    if (selected.length === 0) {
                        return react__WEBPACK_IMPORTED_MODULE_0__.createElement("em", null, noMetricSelected);
                    }
                    return selected.join(', ');
                }, MenuProps: MenuProps, size: "small", name: _helpers_constants__WEBPACK_IMPORTED_MODULE_4__.METRICS_GRAFANA_KEY },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_MenuItem__WEBPACK_IMPORTED_MODULE_5__["default"], { disabled: true, value: "" },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("em", null, noMetricSelected)),
                metrics.map(metric => (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_MenuItem__WEBPACK_IMPORTED_MODULE_5__["default"], { key: metric, value: metric },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Checkbox__WEBPACK_IMPORTED_MODULE_6__["default"], { checked: metricName.includes(metric) }),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_ListItemText__WEBPACK_IMPORTED_MODULE_7__["default"], { primary: metric }))))),
            metricName.length > 0
                ? `${metricName.length} metric${metricName.length > 1 ? 's' : ''} selected.`
                : null)));
}


/***/ }),

/***/ "./lib/components/VerticalLinearStepper.js":
/*!*************************************************!*\
  !*** ./lib/components/VerticalLinearStepper.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ VerticalLinearStepper)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material_Box__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @mui/material/Box */ "./node_modules/@mui/material/Box/Box.js");
/* harmony import */ var _mui_material_Stepper__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @mui/material/Stepper */ "./node_modules/@mui/material/Stepper/Stepper.js");
/* harmony import */ var _mui_material_Step__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @mui/material/Step */ "./node_modules/@mui/material/Step/Step.js");
/* harmony import */ var _mui_material_StepLabel__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @mui/material/StepLabel */ "./node_modules/@mui/material/StepLabel/StepLabel.js");
/* harmony import */ var _mui_material_StepContent__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @mui/material/StepContent */ "./node_modules/@mui/material/StepContent/StepContent.js");
/* harmony import */ var _mui_material_Button__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @mui/material/Button */ "./node_modules/@mui/material/Button/Button.js");
/* harmony import */ var _mui_material_Paper__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @mui/material/Paper */ "./node_modules/@mui/material/Paper/Paper.js");
/* harmony import */ var _mui_material_Typography__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material/Typography */ "./node_modules/@mui/material/Typography/Typography.js");
/* harmony import */ var _progress_CircularWithValueLabel__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./progress/CircularWithValueLabel */ "./lib/components/progress/CircularWithValueLabel.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _table_CollapsibleTable__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./table/CollapsibleTable */ "./lib/components/table/CollapsibleTable.js");
/* harmony import */ var _progress_LinearProgress__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./progress/LinearProgress */ "./lib/components/progress/LinearProgress.js");













const steps = [
    {
        label: 'Approach'
    },
    {
        label: 'Fetch/compute',
        hasButtons: false
    },
    {
        label: 'Visualisation options'
    },
    {
        label: 'Deployment',
        hasButtons: false
    }
];
function StepOne() {
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, null,
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.FormControl, null,
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.RadioGroup, { "aria-labelledby": "demo-radio-buttons-group-label", defaultValue: "pre-compute", name: "radio-buttons-group" },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.FormControlLabel, { value: "pre-compute", control: react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Radio, null), label: "Pre-Compute" }),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.FormControlLabel, { value: "sample", control: react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Radio, null), label: "Sample Computation" }),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.FormControlLabel, { value: "simulation-pred", control: react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Radio, null), label: "Simulation/Prediction" })))));
}
function StepTwo({ handleFinish, label }) {
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, null,
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Typography__WEBPACK_IMPORTED_MODULE_2__["default"], null, label),
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_progress_CircularWithValueLabel__WEBPACK_IMPORTED_MODULE_3__["default"], { onFinish: handleFinish })));
}
function StepThree() {
    return react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null);
}
function StepFour({ handleFinish, label }) {
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, null,
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Button__WEBPACK_IMPORTED_MODULE_4__["default"], { onClick: handleFinish, title: "Reset" })));
}
function ContentHandler({ step, triggerNextStep, handleLastStep }) {
    switch (step) {
        default:
        case 0:
            return react__WEBPACK_IMPORTED_MODULE_0__.createElement(StepOne, null);
        case 1:
            return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(StepTwo, { handleFinish: triggerNextStep, label: "Predicting results..." }));
        case 2:
            return react__WEBPACK_IMPORTED_MODULE_0__.createElement(StepThree, null);
        case 3:
            return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(StepFour, { handleFinish: handleLastStep, label: "Deploying application..." }));
    }
}
function VerticalLinearStepper() {
    const [activeStep, setActiveStep] = react__WEBPACK_IMPORTED_MODULE_0__.useState(0);
    const [complete, setComplete] = react__WEBPACK_IMPORTED_MODULE_0__.useState(false);
    const [checkedIndex, setCheckedIndex] = react__WEBPACK_IMPORTED_MODULE_0__.useState(null);
    const disableNextStepThree = activeStep === 2 && checkedIndex === null;
    const handleNext = () => {
        setActiveStep(prevActiveStep => prevActiveStep + 1);
    };
    const handleBack = () => {
        setActiveStep(prevActiveStep => prevActiveStep - (prevActiveStep === 2 ? 2 : 1));
    };
    const handleReset = () => {
        setActiveStep(0);
        setComplete(false);
    };
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, { sx: { display: 'flex', width: '100%', height: '500px' } },
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, null,
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Stepper__WEBPACK_IMPORTED_MODULE_5__["default"], { activeStep: activeStep, orientation: "vertical" }, steps.map((step, index) => (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Step__WEBPACK_IMPORTED_MODULE_6__["default"], { key: step.label },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_StepLabel__WEBPACK_IMPORTED_MODULE_7__["default"], { optional: index === steps.length - 1 ? (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Typography__WEBPACK_IMPORTED_MODULE_2__["default"], { variant: "caption" }, "Last step")) : null }, step.label),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_StepContent__WEBPACK_IMPORTED_MODULE_8__["default"], null,
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(ContentHandler, { step: activeStep, triggerNextStep: handleNext, handleLastStep: handleReset }),
                    step.hasButtons !== false && (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Box__WEBPACK_IMPORTED_MODULE_9__["default"], { sx: { mb: 2 } },
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Button__WEBPACK_IMPORTED_MODULE_4__["default"], { variant: "contained", onClick: handleNext, sx: { mt: 1, mr: 1 }, disabled: disableNextStepThree }, index === steps.length - 1 ? 'Finish' : 'Continue'),
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Button__WEBPACK_IMPORTED_MODULE_4__["default"], { disabled: index === 0, onClick: handleBack, sx: { mt: 1, mr: 1 } }, "Back"))))))))),
        activeStep === 2 && (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Paper__WEBPACK_IMPORTED_MODULE_10__["default"], { square: true, elevation: 0, sx: { p: 3, width: '100%', overflow: 'visible' } },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_table_CollapsibleTable__WEBPACK_IMPORTED_MODULE_11__["default"], { checkedIndex: checkedIndex, setCheckedIndex: setCheckedIndex }))),
        activeStep === 3 && (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, { sx: { width: '400px' } }, complete ? (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, { sx: { display: 'flex', justifyContent: 'center' } },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Typography__WEBPACK_IMPORTED_MODULE_2__["default"], null, "Deployment complete!"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Button__WEBPACK_IMPORTED_MODULE_4__["default"], { title: "Reset", onClick: handleReset }))) : (react__WEBPACK_IMPORTED_MODULE_0__.createElement(react__WEBPACK_IMPORTED_MODULE_0__.Fragment, null,
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Typography__WEBPACK_IMPORTED_MODULE_2__["default"], null, "Deploying..."),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_progress_LinearProgress__WEBPACK_IMPORTED_MODULE_12__["default"], { setComplete: () => setComplete(true) })))))));
}


/***/ }),

/***/ "./lib/components/progress/CircularWithValueLabel.js":
/*!***********************************************************!*\
  !*** ./lib/components/progress/CircularWithValueLabel.js ***!
  \***********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ CircularWithValueLabel)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material_CircularProgress__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material/CircularProgress */ "./node_modules/@mui/material/CircularProgress/CircularProgress.js");
/* harmony import */ var _mui_material_Typography__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @mui/material/Typography */ "./node_modules/@mui/material/Typography/Typography.js");
/* harmony import */ var _mui_material_Box__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material/Box */ "./node_modules/@mui/material/Box/Box.js");




function CircularProgressWithLabel(props) {
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Box__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: { position: 'relative', display: 'inline-flex' } },
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_CircularProgress__WEBPACK_IMPORTED_MODULE_2__["default"], { variant: "determinate", ...props }),
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Box__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: {
                top: 0,
                left: 0,
                bottom: 0,
                right: 0,
                position: 'absolute',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
            } },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Typography__WEBPACK_IMPORTED_MODULE_3__["default"], { variant: "caption", component: "div", sx: { color: 'text.secondary' } }, `${Math.round(props.value)}%`))));
}
function CircularWithValueLabel({ onFinish }) {
    const [progress, setProgress] = react__WEBPACK_IMPORTED_MODULE_0__.useState(10);
    function handleConclusion() {
        onFinish();
        return 0;
    }
    react__WEBPACK_IMPORTED_MODULE_0__.useEffect(() => {
        const timer = setInterval(() => {
            setProgress(prevProgress => prevProgress >= 100 ? handleConclusion() : prevProgress + 10);
        }, 400);
        return () => {
            clearInterval(timer);
        };
    }, []);
    return react__WEBPACK_IMPORTED_MODULE_0__.createElement(CircularProgressWithLabel, { value: progress });
}


/***/ }),

/***/ "./lib/components/progress/LinearProgress.js":
/*!***************************************************!*\
  !*** ./lib/components/progress/LinearProgress.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ LinearBuffer)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material_Box__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material/Box */ "./node_modules/@mui/material/Box/Box.js");
/* harmony import */ var _mui_material_LinearProgress__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material/LinearProgress */ "./node_modules/@mui/material/LinearProgress/LinearProgress.js");



function LinearBuffer({ setComplete }) {
    const [progress, setProgress] = react__WEBPACK_IMPORTED_MODULE_0__.useState(0);
    const [buffer, setBuffer] = react__WEBPACK_IMPORTED_MODULE_0__.useState(10);
    const progressRef = react__WEBPACK_IMPORTED_MODULE_0__.useRef(() => { });
    react__WEBPACK_IMPORTED_MODULE_0__.useEffect(() => {
        progressRef.current = () => {
            if (progress === 100) {
                setComplete();
            }
            else {
                setProgress(progress + 1);
                if (buffer < 100 && progress % 5 === 0) {
                    const newBuffer = buffer + 1 + Math.random() * 10;
                    setBuffer(newBuffer > 100 ? 100 : newBuffer);
                }
            }
        };
    });
    react__WEBPACK_IMPORTED_MODULE_0__.useEffect(() => {
        const timer = setInterval(() => {
            progressRef.current();
        }, 50);
        return () => {
            clearInterval(timer);
        };
    }, []);
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Box__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: { width: '100%' } },
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_LinearProgress__WEBPACK_IMPORTED_MODULE_2__["default"], { variant: "buffer", value: progress, valueBuffer: buffer })));
}


/***/ }),

/***/ "./lib/components/table/CollapsibleTable.js":
/*!**************************************************!*\
  !*** ./lib/components/table/CollapsibleTable.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ CollapsibleTable)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material_Box__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @mui/material/Box */ "./node_modules/@mui/material/Box/Box.js");
/* harmony import */ var _mui_material_Collapse__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @mui/material/Collapse */ "./node_modules/@mui/material/Collapse/Collapse.js");
/* harmony import */ var _mui_material_IconButton__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @mui/material/IconButton */ "./node_modules/@mui/material/IconButton/IconButton.js");
/* harmony import */ var _mui_material_Table__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @mui/material/Table */ "./node_modules/@mui/material/Table/Table.js");
/* harmony import */ var _mui_material_TableBody__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @mui/material/TableBody */ "./node_modules/@mui/material/TableBody/TableBody.js");
/* harmony import */ var _mui_material_TableCell__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @mui/material/TableCell */ "./node_modules/@mui/material/TableCell/TableCell.js");
/* harmony import */ var _mui_material_TableContainer__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @mui/material/TableContainer */ "./node_modules/@mui/material/TableContainer/TableContainer.js");
/* harmony import */ var _mui_material_TableHead__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @mui/material/TableHead */ "./node_modules/@mui/material/TableHead/TableHead.js");
/* harmony import */ var _mui_material_TableRow__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material/TableRow */ "./node_modules/@mui/material/TableRow/TableRow.js");
/* harmony import */ var _mui_material_Typography__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @mui/material/Typography */ "./node_modules/@mui/material/Typography/Typography.js");
/* harmony import */ var _mui_material_Paper__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @mui/material/Paper */ "./node_modules/@mui/material/Paper/Paper.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _mui_icons_material_KeyboardArrowDown__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @mui/icons-material/KeyboardArrowDown */ "./node_modules/@mui/icons-material/esm/KeyboardArrowDown.js");
/* harmony import */ var _mui_icons_material_KeyboardArrowUp__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @mui/icons-material/KeyboardArrowUp */ "./node_modules/@mui/icons-material/esm/KeyboardArrowUp.js");

// import PropTypes from 'prop-types';














function createData(sci, time, availability) {
    const datacentres = Array.from({ length: 2 }, (_, index) => ({
        label: `Data Centre ${index + 1}`,
        details: {
            cpu: {
                usage: Number((Math.random() * 100).toFixed(2)),
                time: Math.floor(Math.random() * 10000),
                frequency: Number((Math.random() * 3 + 2).toFixed(2))
            },
            memory: {
                energy: Number((Math.random() * 1000).toFixed(2)),
                used: Math.floor(Math.random() * 1000000)
            },
            network: {
                io: Number((Math.random() * 100).toFixed(2)),
                connections: Math.floor(Math.random() * 50)
            }
        }
    }));
    return { sci, time, availability, datacentres };
}
function Row({ row, checkedIndex, setSelectedIndex, rowIndex }) {
    const [open, setOpen] = react__WEBPACK_IMPORTED_MODULE_0___default().useState(false);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableRow__WEBPACK_IMPORTED_MODULE_2__["default"], null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableCell__WEBPACK_IMPORTED_MODULE_3__["default"], null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, { sx: { display: 'flex', alignItems: 'center' } },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Typography__WEBPACK_IMPORTED_MODULE_4__["default"], null, rowIndex),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_IconButton__WEBPACK_IMPORTED_MODULE_5__["default"], { "aria-label": "expand row", size: "small", onClick: () => setOpen(!open) }, open ? react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_KeyboardArrowUp__WEBPACK_IMPORTED_MODULE_6__["default"], null) : react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_KeyboardArrowDown__WEBPACK_IMPORTED_MODULE_7__["default"], null)),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Checkbox, { checked: checkedIndex, onClick: setSelectedIndex }))),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableCell__WEBPACK_IMPORTED_MODULE_3__["default"], null, row.sci),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableCell__WEBPACK_IMPORTED_MODULE_3__["default"], { align: "right" }, row.time),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableCell__WEBPACK_IMPORTED_MODULE_3__["default"], { align: "center" }, row.availability)),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableRow__WEBPACK_IMPORTED_MODULE_2__["default"], null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableCell__WEBPACK_IMPORTED_MODULE_3__["default"], { style: { paddingBottom: 0, paddingTop: 0 }, colSpan: 4 },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Collapse__WEBPACK_IMPORTED_MODULE_8__["default"], { in: open, timeout: "auto", unmountOnExit: true },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Box__WEBPACK_IMPORTED_MODULE_9__["default"], { sx: { m: 1 } }, row.datacentres.map((datacentre, index) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Box__WEBPACK_IMPORTED_MODULE_9__["default"], { key: index, sx: {
                            mb: 2,
                            border: '1px solid #ddd',
                            borderRadius: '8px',
                            p: 2
                        } },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Typography__WEBPACK_IMPORTED_MODULE_4__["default"], { sx: { fontWeight: 'bold', mb: 1 }, variant: "subtitle1" }, datacentre.label),
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, { container: true, spacing: 2, sx: { display: 'flex', justifyContent: 'space-between' } },
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, { sx: {
                                    display: 'flex',
                                    flexDirection: 'column',
                                    flexGrow: 1
                                } },
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Typography__WEBPACK_IMPORTED_MODULE_4__["default"], { sx: { fontWeight: 'bold' } }, "CPU"),
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("ul", { style: { paddingInlineStart: '10px' } },
                                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", null,
                                        "Usage: ",
                                        datacentre.details.cpu.usage,
                                        " %"),
                                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", null,
                                        "Time: ",
                                        datacentre.details.cpu.time,
                                        " \u03BCs"),
                                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", null,
                                        "Frequency: ",
                                        datacentre.details.cpu.frequency,
                                        " GHz"))),
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, { sx: {
                                    display: 'flex',
                                    flexDirection: 'column',
                                    flexGrow: 1
                                } },
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Typography__WEBPACK_IMPORTED_MODULE_4__["default"], { sx: { fontWeight: 'bold' } }, "Memory"),
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("ul", { style: { paddingInlineStart: '10px' } },
                                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", null,
                                        "Energy: ",
                                        datacentre.details.memory.energy,
                                        " \u03BCJ"),
                                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", null,
                                        "Used: ",
                                        datacentre.details.memory.used,
                                        " Bytes"))),
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, { sx: {
                                    display: 'flex',
                                    flexDirection: 'column',
                                    flexGrow: 1
                                } },
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Typography__WEBPACK_IMPORTED_MODULE_4__["default"], { sx: { fontWeight: 'bold' } }, "Network"),
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("ul", { style: { paddingInlineStart: '10px' } },
                                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", null,
                                        "IO: ",
                                        datacentre.details.network.io,
                                        " B/s"),
                                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", null,
                                        "Connections: ",
                                        datacentre.details.network.connections)))))))))))));
}
const rows = [
    createData(12.33, 4500, '++'),
    createData(14.12, 5200, '+'),
    createData(10.89, 4300, '+++')
];
function CollapsibleTable({ checkedIndex, setCheckedIndex }) {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableContainer__WEBPACK_IMPORTED_MODULE_10__["default"], { component: _mui_material_Paper__WEBPACK_IMPORTED_MODULE_11__["default"] },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Table__WEBPACK_IMPORTED_MODULE_12__["default"], { "aria-label": "collapsible table" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableHead__WEBPACK_IMPORTED_MODULE_13__["default"], null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableRow__WEBPACK_IMPORTED_MODULE_2__["default"], null,
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableCell__WEBPACK_IMPORTED_MODULE_3__["default"], null),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableCell__WEBPACK_IMPORTED_MODULE_3__["default"], null, "SCI"),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableCell__WEBPACK_IMPORTED_MODULE_3__["default"], { align: "right" }, "Est. Time (s)"),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableCell__WEBPACK_IMPORTED_MODULE_3__["default"], { align: "center" }, "Availability"))),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableBody__WEBPACK_IMPORTED_MODULE_14__["default"], null, rows.map((row, index) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(Row, { key: index, row: row, rowIndex: index, checkedIndex: index === checkedIndex, setSelectedIndex: () => {
                    const newValue = index === checkedIndex ? null : index;
                    setCheckedIndex(newValue);
                } })))))));
}


/***/ }),

/***/ "./lib/dialog/CreateChartDialog.js":
/*!*****************************************!*\
  !*** ./lib/dialog/CreateChartDialog.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ CreateChartDialog)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material_Button__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @mui/material/Button */ "./node_modules/@mui/material/Button/Button.js");
/* harmony import */ var _mui_material_TextField__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @mui/material/TextField */ "./node_modules/@mui/material/TextField/TextField.js");
/* harmony import */ var _mui_material_Dialog__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material/Dialog */ "./node_modules/@mui/material/Dialog/Dialog.js");
/* harmony import */ var _mui_material_DialogActions__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @mui/material/DialogActions */ "./node_modules/@mui/material/DialogActions/DialogActions.js");
/* harmony import */ var _mui_material_DialogContent__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @mui/material/DialogContent */ "./node_modules/@mui/material/DialogContent/DialogContent.js");
/* harmony import */ var _mui_material_DialogContentText__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @mui/material/DialogContentText */ "./node_modules/@mui/material/DialogContentText/DialogContentText.js");
/* harmony import */ var _mui_material_DialogTitle__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @mui/material/DialogTitle */ "./node_modules/@mui/material/DialogTitle/DialogTitle.js");
/* harmony import */ var _components_SelectComponent__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../components/SelectComponent */ "./lib/components/SelectComponent.js");
/* harmony import */ var _helpers_constants__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../helpers/constants */ "./lib/helpers/constants.js");










const isValidUrl = (urlString) => {
    const urlPattern = new RegExp('^(http?:\\/\\/)?' + // validate protocol
        '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' + // validate domain name
        '((\\d{1,3}\\.){3}\\d{1,3}))' + // validate OR ip (v4) address
        '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' + // validate port and path
        '(\\?[;&a-z\\d%_.~+=-]*)?' + // validate query string
        '(\\#[-a-z\\d_]*)?$', 'i'); // validate fragment locator
    return !!urlPattern.test(urlString);
};
function CreateChartDialog({ open, handleClose, sendNewMetrics, sendNewUrl }) {
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(react__WEBPACK_IMPORTED_MODULE_0__.Fragment, null,
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Dialog__WEBPACK_IMPORTED_MODULE_1__["default"], { open: open, onClose: (_e, reason) => {
                if (reason === 'backdropClick' || reason === 'escapeKeyDown') {
                    return;
                }
                else {
                    handleClose(true);
                }
            }, slotProps: {
                paper: {
                    component: 'form',
                    onSubmit: (event) => {
                        event.preventDefault();
                        const formData = new FormData(event.currentTarget);
                        const formJson = Object.fromEntries(formData.entries());
                        if (_helpers_constants__WEBPACK_IMPORTED_MODULE_2__.METRICS_GRAFANA_KEY in formJson) {
                            const metrics = formJson.metrics_grafana;
                            sendNewMetrics(metrics.split(','));
                        }
                        if (_helpers_constants__WEBPACK_IMPORTED_MODULE_2__.URL_GRAFANA_KEY in formJson) {
                            const url = formJson.url_grafana;
                            // Only send the URl if it is valid, since it is optional.
                            if (isValidUrl(url)) {
                                sendNewUrl(url);
                            }
                        }
                        else {
                            throw 'Some error happened with the form.';
                        }
                    }
                }
            } },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_DialogTitle__WEBPACK_IMPORTED_MODULE_3__["default"], null, "Add Metric Chart"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_DialogContent__WEBPACK_IMPORTED_MODULE_4__["default"], null,
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_DialogContentText__WEBPACK_IMPORTED_MODULE_5__["default"], null, "To create a chart, you must either select a metric from the list, and/or provide the URL from the Grafana's dashboard."),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_SelectComponent__WEBPACK_IMPORTED_MODULE_6__["default"], null),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_TextField__WEBPACK_IMPORTED_MODULE_7__["default"], { autoFocus: true, 
                    // required
                    margin: "dense", id: "name", name: _helpers_constants__WEBPACK_IMPORTED_MODULE_2__.URL_GRAFANA_KEY, label: "Grafana URL", type: "url", fullWidth: true, variant: "outlined", size: "small" })),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_DialogActions__WEBPACK_IMPORTED_MODULE_8__["default"], null,
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Button__WEBPACK_IMPORTED_MODULE_9__["default"], { onClick: () => handleClose(true), sx: { textTransform: 'none' } }, "Cancel"),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Button__WEBPACK_IMPORTED_MODULE_9__["default"], { type: "submit", sx: { textTransform: 'none' } }, "Create")))));
}


/***/ }),

/***/ "./lib/helpers/constants.js":
/*!**********************************!*\
  !*** ./lib/helpers/constants.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DEFAULT_REFRESH_RATE: () => (/* binding */ DEFAULT_REFRESH_RATE),
/* harmony export */   METRICS_GRAFANA_KEY: () => (/* binding */ METRICS_GRAFANA_KEY),
/* harmony export */   URL_GRAFANA_KEY: () => (/* binding */ URL_GRAFANA_KEY)
/* harmony export */ });
const DEFAULT_REFRESH_RATE = 2;
const URL_GRAFANA_KEY = 'url_grafana';
const METRICS_GRAFANA_KEY = 'metrics_grafana';


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");



/**
 * Main reference: https://github.com/jupyterlab/extension-examples/blob/71486d7b891175fb3883a8b136b8edd2cd560385/react/react-widget/src/index.ts
 * And all other files in the repo.
 */
const namespaceId = 'gdapod';
/**
 * Initialization data for the GreenDIGIT JupyterLab extension.
 */
const plugin = {
    id: 'jupyterlab-greendigit',
    description: 'GreenDIGIT App',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    activate: async (app, palette, restorer) => {
        console.log('JupyterLab extension GreenDIGIT is activated!');
        const { shell } = app;
        // Create a widget tracker
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace: namespaceId
        });
        // Ensure the tracker is restored properly on refresh
        restorer.restore(tracker, {
            command: `${namespaceId}:open`,
            name: () => 'greendigit-jupyterlab'
            // when: app.restored, // Ensure restorer waits for the app to be fully restored
        });
        // Define a widget creator function
        const newWidget = async () => {
            const content = new _widget__WEBPACK_IMPORTED_MODULE_2__.MainWidget();
            const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content });
            widget.id = 'greendigit-jupyterlab';
            widget.title.label = 'GreenDIGIT Dashboard';
            widget.title.closable = true;
            return widget;
        };
        // Add an application command
        const openCommand = `${namespaceId}:open`;
        app.commands.addCommand(openCommand, {
            label: 'Open GreenDIGIT Dashboard',
            execute: async () => {
                let widget = tracker.currentWidget;
                if (!widget || widget.isDisposed) {
                    widget = await newWidget();
                    // Add the widget to the tracker and shell
                    tracker.add(widget);
                    shell.add(widget, 'main');
                }
                if (!widget.isAttached) {
                    shell.add(widget, 'main');
                }
                shell.activateById(widget.id);
            }
        });
        // Add the command to the palette
        palette.addItem({ command: openCommand, category: 'Sustainability' });
        // Restore the widget if available
        if (!tracker.currentWidget) {
            const widget = await newWidget();
            tracker.add(widget);
            shell.add(widget, 'main');
        }
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/pages/ChartsPage.js":
/*!*********************************!*\
  !*** ./lib/pages/ChartsPage.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ ChartsPage)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _components_AddButton__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../components/AddButton */ "./lib/components/AddButton.js");
/* harmony import */ var _dialog_CreateChartDialog__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../dialog/CreateChartDialog */ "./lib/dialog/CreateChartDialog.js");
/* harmony import */ var _components_ChartWrapper__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../components/ChartWrapper */ "./lib/components/ChartWrapper.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_GoBackButton__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../components/GoBackButton */ "./lib/components/GoBackButton.js");






const CONFIG_BASE_URL = 'http://localhost:3000/';
const DEFAULT_SRC_IFRAME = `${CONFIG_BASE_URL}d-solo/behmsglt2r08wa/memory-and-cpu?orgId=1&from=1743616284487&to=1743621999133&timezone=browser&theme=light&panelId=1&__feature.dashboardSceneSolo`;
function ChartsPage({ handleGoBack }) {
    const [iframeMap, setIFrameMap] = react__WEBPACK_IMPORTED_MODULE_0___default().useState(new Map());
    const [createChartOpen, setCreateChartOpen] = react__WEBPACK_IMPORTED_MODULE_0___default().useState(false);
    function handleDeleteIFrame(keyId) {
        setIFrameMap(prevMap => {
            const newMap = new Map(prevMap);
            newMap === null || newMap === void 0 ? void 0 : newMap.delete(keyId);
            return newMap;
        });
    }
    function createIFrame({ src, height, width, keyId }) {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_ChartWrapper__WEBPACK_IMPORTED_MODULE_2__["default"], { keyId: keyId, src: src, width: width, height: height, onDelete: handleDeleteIFrame }));
    }
    function createChart(newUrl) {
        const newKeyId = Number(String(Date.now()) + String(Math.round(Math.random() * 10000)));
        const iframe = createIFrame({
            src: newUrl !== null && newUrl !== void 0 ? newUrl : DEFAULT_SRC_IFRAME,
            height: 400,
            width: 600,
            keyId: newKeyId
        });
        return [newKeyId, iframe];
    }
    function handleOpenCreateChartDialog() {
        setCreateChartOpen(true);
    }
    function handleNewMetrics(newMetrics) {
        const newMap = new Map(iframeMap);
        for (let i = 0; i < newMetrics.length; i++) {
            newMap.set(...createChart(DEFAULT_SRC_IFRAME));
        }
        setIFrameMap(newMap);
        setCreateChartOpen(false);
    }
    function handleSubmitUrl(newUrl) {
        const newMap = new Map(iframeMap);
        newMap.set(...createChart(newUrl));
        // setIFrameMap(newMap);
    }
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, { sx: { display: 'flex', flexDirection: 'column' } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, { sx: { display: 'flex' } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_GoBackButton__WEBPACK_IMPORTED_MODULE_3__["default"], { handleClick: handleGoBack })),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_AddButton__WEBPACK_IMPORTED_MODULE_4__["default"], { handleClickButton: handleOpenCreateChartDialog }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, { sx: { display: 'flex', flexDirection: 'row' } }, iframeMap ? iframeMap.values() : null),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_dialog_CreateChartDialog__WEBPACK_IMPORTED_MODULE_5__["default"], { open: createChartOpen, handleClose: (isCancel) => isCancel && setCreateChartOpen(false), sendNewMetrics: handleNewMetrics, sendNewUrl: (url) => handleSubmitUrl(url) })));
}


/***/ }),

/***/ "./lib/pages/GeneralDashboard.js":
/*!***************************************!*\
  !*** ./lib/pages/GeneralDashboard.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ GeneralDashboard)
/* harmony export */ });
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);


// import BandHighLight from '../components/BandHighLight';
// import ElementHighlights from '../components/ElementHighlights';
// import MapComponent from '../components/map/MapComponent';
/**
 * This is something temporary. Just for the demo on April 8th, on All-Hands Meeting for GreenDIGIT.
 */
const chartLinks = [
    // CPU Usage: used and total
    'http://localhost:3000/d-solo/behmsglt2r08wa/2025-04-08-demo?orgId=1&from=1743669689152&to=1743691289152&timezone=browser&theme=light&panelId=2&__feature.dashboardSceneSolo',
    // Memory used
    'http://localhost:3000/d-solo/behmsglt2r08wa/2025-04-08-demo?orgId=1&from=1743669689152&to=1743691289152&timezone=browser&theme=light&panelId=3&__feature.dashboardSceneSolo',
    // Network received/sent
    'http://localhost:3000/d-solo/behmsglt2r08wa/2025-04-08-demo?orgId=1&from=1743669689152&to=1743691289152&timezone=browser&theme=light&panelId=4&__feature.dashboardSceneSolo',
    // Thread Nr.
    'http://localhost:3000/d-solo/behmsglt2r08wa/2025-04-08-demo?orgId=1&from=1743670340144&to=1743691940144&timezone=browser&theme=light&panelId=5&__feature.dashboardSceneSolo'
];
const styles = {
    main: {
        display: 'flex',
        flexDirection: 'row',
        width: '100%',
        height: '100%',
        flexWrap: 'wrap',
        boxSizing: 'border-box',
        padding: '10px',
        whiteSpace: 'nowrap'
    },
    grid: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center'
        // flex: '0 1 50%'
        // width: '50%'
        // border: '1px solid green',
        // boxSizing: 'border-box',
    }
};
function TempIframe({ keyIndex, url }) {
    return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("iframe", { src: url, width: "100%", height: "400px", sandbox: "allow-scripts allow-same-origin", 
        // ref={iframeRef}
        id: `iframe-item-${keyIndex}`, style: { border: 'none', margin: '5px' } }));
}
function GeneralDashboard() {
    function GridContent({ index }) {
        return react__WEBPACK_IMPORTED_MODULE_1___default().createElement(TempIframe, { keyIndex: index, url: chartLinks[index] });
        // switch (index) {
        //   case 1:
        //     return <TempIframe keyIndex={1} />;
        //   case 2:
        //     return <TempIframe keyIndex={2} />;
        //   case 3:
        //     return <MapComponent />;
        //   default:
        //     return <span>{'Grid element ' + String(index)}</span>;
        // }
    }
    const gridElements = Array.from(new Array(chartLinks.length));
    return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { style: styles.main }, gridElements.map((value, index) => {
        return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_0__.Paper, { key: `grid-element-${value}`, style: {
                ...styles.grid
                // minWidth: value === 3 ? '100%' : '50%',
                // flex: value === 3 ? '0 1 100%' : '0 1 50%'
            } },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(GridContent, { index: index })));
    })));
}


/***/ }),

/***/ "./lib/pages/WelcomePage.js":
/*!**********************************!*\
  !*** ./lib/pages/WelcomePage.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ WelcomePage)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _GeneralDashboard__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./GeneralDashboard */ "./lib/pages/GeneralDashboard.js");



const styles = {
    main: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        width: '100%'
    },
    title: {
        my: 2
    },
    buttonGrid: {
        display: 'flex',
        width: '100%',
        gap: 3,
        justifyContent: 'center',
        alignContent: 'center',
        '& .MuiButtonBase-root': {
            textTransform: 'none'
        },
        mb: 2
    }
};
function WelcomePage({ handleRealTimeClick, handlePredictionClick }) {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, { sx: styles.main },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Typography, { variant: "h4", sx: styles.title }, "Welcome to GreenDIGIT Dashboard"),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, { sx: styles.buttonGrid },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Button, { variant: "outlined", onClick: handleRealTimeClick }, "Real-time Tracking Monitor"),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Button, { variant: "outlined", onClick: handlePredictionClick }, "Resource Usage Prediction")),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_GeneralDashboard__WEBPACK_IMPORTED_MODULE_2__["default"], null)));
}


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   MainWidget: () => (/* binding */ MainWidget),
/* harmony export */   Page: () => (/* binding */ Page)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _pages_ChartsPage__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./pages/ChartsPage */ "./lib/pages/ChartsPage.js");
/* harmony import */ var _pages_WelcomePage__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./pages/WelcomePage */ "./lib/pages/WelcomePage.js");
/* harmony import */ var _components_VerticalLinearStepper__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./components/VerticalLinearStepper */ "./lib/components/VerticalLinearStepper.js");
/* harmony import */ var _components_GoBackButton__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./components/GoBackButton */ "./lib/components/GoBackButton.js");







const styles = {
    main: {
        display: 'flex',
        flexDirection: 'row',
        width: '100%',
        height: '100%',
        flexWrap: 'wrap',
        boxSizing: 'border-box',
        padding: '3px'
    },
    grid: {
        display: 'flex',
        flexDirection: 'column',
        whiteSpace: 'wrap',
        // justifyContent: 'center',
        // alignItems: 'center',
        flex: '0 1 100%',
        width: '100%',
        height: '100%',
        overflow: 'auto',
        padding: '10px'
    }
};
function Prediction({ handleGoBack }) {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_2__.Grid2, { sx: { width: '100%', px: 3, py: 5 } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_GoBackButton__WEBPACK_IMPORTED_MODULE_3__["default"], { handleClick: handleGoBack }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_VerticalLinearStepper__WEBPACK_IMPORTED_MODULE_4__["default"], null)));
}
var Page;
(function (Page) {
    Page[Page["WelcomePage"] = 0] = "WelcomePage";
    Page[Page["ChartsPage"] = 1] = "ChartsPage";
    Page[Page["Prediction"] = 2] = "Prediction";
})(Page || (Page = {}));
/**
 * React component for a counter.
 *
 * @returns The React component
 */
const App = () => {
    const [activePageState, setActivePageState] = react__WEBPACK_IMPORTED_MODULE_0___default().useState(Page.WelcomePage);
    function handleRealTimeClick() {
        setActivePageState(Page.ChartsPage);
    }
    function handlePredictionClick() {
        setActivePageState(Page.Prediction);
    }
    function goToMainPage() {
        setActivePageState(Page.WelcomePage);
    }
    const ActivePage = {
        [Page.WelcomePage]: (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_pages_WelcomePage__WEBPACK_IMPORTED_MODULE_5__["default"], { handleRealTimeClick: handleRealTimeClick, handlePredictionClick: handlePredictionClick })),
        [Page.ChartsPage]: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_pages_ChartsPage__WEBPACK_IMPORTED_MODULE_6__["default"], { handleGoBack: goToMainPage }),
        [Page.Prediction]: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(Prediction, { handleGoBack: goToMainPage })
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { style: styles.main },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_2__.Paper, { style: styles.grid }, ActivePage[activePageState])));
};
/**
 * A Counter Lumino Widget that wraps a CounterComponent.
 */
class MainWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    /**
     * Constructs a new CounterWidget.
     */
    constructor() {
        super();
        this.addClass('jp-ReactWidget');
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(App, null);
    }
}


/***/ }),

/***/ "./node_modules/@mui/icons-material/esm/AddCircleOutlineRounded.js":
/*!*************************************************************************!*\
  !*** ./node_modules/@mui/icons-material/esm/AddCircleOutlineRounded.js ***!
  \*************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils/createSvgIcon.js */ "./node_modules/@mui/material/utils/createSvgIcon.js");
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "./node_modules/react/jsx-runtime.js");
"use client";



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ((0,_utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__["default"])(/*#__PURE__*/(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("path", {
  d: "M12 7c-.55 0-1 .45-1 1v3H8c-.55 0-1 .45-1 1s.45 1 1 1h3v3c0 .55.45 1 1 1s1-.45 1-1v-3h3c.55 0 1-.45 1-1s-.45-1-1-1h-3V8c0-.55-.45-1-1-1m0-5C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2m0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8"
}), 'AddCircleOutlineRounded'));

/***/ }),

/***/ "./node_modules/@mui/icons-material/esm/ArrowBackRounded.js":
/*!******************************************************************!*\
  !*** ./node_modules/@mui/icons-material/esm/ArrowBackRounded.js ***!
  \******************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils/createSvgIcon.js */ "./node_modules/@mui/material/utils/createSvgIcon.js");
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "./node_modules/react/jsx-runtime.js");
"use client";



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ((0,_utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__["default"])(/*#__PURE__*/(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("path", {
  d: "M19 11H7.83l4.88-4.88c.39-.39.39-1.03 0-1.42a.996.996 0 0 0-1.41 0l-6.59 6.59c-.39.39-.39 1.02 0 1.41l6.59 6.59c.39.39 1.02.39 1.41 0s.39-1.02 0-1.41L7.83 13H19c.55 0 1-.45 1-1s-.45-1-1-1"
}), 'ArrowBackRounded'));

/***/ }),

/***/ "./node_modules/@mui/icons-material/esm/DeleteOutlineRounded.js":
/*!**********************************************************************!*\
  !*** ./node_modules/@mui/icons-material/esm/DeleteOutlineRounded.js ***!
  \**********************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils/createSvgIcon.js */ "./node_modules/@mui/material/utils/createSvgIcon.js");
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "./node_modules/react/jsx-runtime.js");
"use client";



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ((0,_utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__["default"])(/*#__PURE__*/(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("path", {
  d: "M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2H8c-1.1 0-2 .9-2 2zM9 9h6c.55 0 1 .45 1 1v8c0 .55-.45 1-1 1H9c-.55 0-1-.45-1-1v-8c0-.55.45-1 1-1m6.5-5-.71-.71c-.18-.18-.44-.29-.7-.29H9.91c-.26 0-.52.11-.7.29L8.5 4H6c-.55 0-1 .45-1 1s.45 1 1 1h12c.55 0 1-.45 1-1s-.45-1-1-1z"
}), 'DeleteOutlineRounded'));

/***/ }),

/***/ "./node_modules/@mui/icons-material/esm/KeyboardArrowDown.js":
/*!*******************************************************************!*\
  !*** ./node_modules/@mui/icons-material/esm/KeyboardArrowDown.js ***!
  \*******************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils/createSvgIcon.js */ "./node_modules/@mui/material/utils/createSvgIcon.js");
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "./node_modules/react/jsx-runtime.js");
"use client";



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ((0,_utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__["default"])(/*#__PURE__*/(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("path", {
  d: "M7.41 8.59 12 13.17l4.59-4.58L18 10l-6 6-6-6z"
}), 'KeyboardArrowDown'));

/***/ }),

/***/ "./node_modules/@mui/icons-material/esm/KeyboardArrowUp.js":
/*!*****************************************************************!*\
  !*** ./node_modules/@mui/icons-material/esm/KeyboardArrowUp.js ***!
  \*****************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils/createSvgIcon.js */ "./node_modules/@mui/material/utils/createSvgIcon.js");
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "./node_modules/react/jsx-runtime.js");
"use client";



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ((0,_utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__["default"])(/*#__PURE__*/(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("path", {
  d: "M7.41 15.41 12 10.83l4.59 4.58L18 14l-6-6-6 6z"
}), 'KeyboardArrowUp'));

/***/ }),

/***/ "./node_modules/@mui/icons-material/esm/RefreshRounded.js":
/*!****************************************************************!*\
  !*** ./node_modules/@mui/icons-material/esm/RefreshRounded.js ***!
  \****************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils/createSvgIcon.js */ "./node_modules/@mui/material/utils/createSvgIcon.js");
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "./node_modules/react/jsx-runtime.js");
"use client";



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ((0,_utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__["default"])(/*#__PURE__*/(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("path", {
  d: "M17.65 6.35c-1.63-1.63-3.94-2.57-6.48-2.31-3.67.37-6.69 3.35-7.1 7.02C3.52 15.91 7.27 20 12 20c3.19 0 5.93-1.87 7.21-4.56.32-.67-.16-1.44-.9-1.44-.37 0-.72.2-.88.53-1.13 2.43-3.84 3.97-6.8 3.31-2.22-.49-4.01-2.3-4.48-4.52C5.31 9.44 8.26 6 12 6c1.66 0 3.14.69 4.22 1.78l-1.51 1.51c-.63.63-.19 1.71.7 1.71H19c.55 0 1-.45 1-1V6.41c0-.89-1.08-1.34-1.71-.71z"
}), 'RefreshRounded'));

/***/ })

}]);
//# sourceMappingURL=lib_index_js.4300b0bf7b04b79d3869.js.map