const ACTION_BUTTON_DELIMITER = "___";
const MORE_THAN_TWO_DECIMAL_PLACES = /^\d*[.,]\d{3,}$/;
const SPINNER = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>';
const CHATBOT_RESPONSE_SPINNER = '<div class="spinner-grow spinner-grow-sm" role="status"><span class="sr-only"></span></div>';

function roundInputFieldValueToTwoDecimalPlaces(inputFieldElem) {
  if (MORE_THAN_TWO_DECIMAL_PLACES.test(inputFieldElem.value)) {
    inputFieldElem.value = parseFloat(inputFieldElem.value).toFixed(2);
  }
}

function clipMinInputFieldValue(inputFieldElem, minValue) {
  if (typeof minValue !== "number" || isNaN(minValue) || !isFinite(minValue)) {
    return;
  }
  if (parseFloat(inputFieldElem.value) < minValue) {
    inputFieldElem.value = minValue;
  }
}

function clipMaxInputFieldValue(inputFieldElem, maxValue) {
  if (typeof maxValue !== "number" || isNaN(maxValue) || !isFinite(maxValue)) {
    return;
  }
  if (parseFloat(inputFieldElem.value) > maxValue) {
    inputFieldElem.value = maxValue;
  }
}

function correctInputFieldValue(inputFieldElem, minValue, maxValue) {
  roundInputFieldValueToTwoDecimalPlaces(inputFieldElem);
  clipMinInputFieldValue(inputFieldElem, minValue);
  clipMaxInputFieldValue(inputFieldElem, maxValue);
}

function countSelectedOptionsMultipleSelectField(elem) {
  if (elem.childElementCount !== 0) {
    return Array.from(elem.children).filter((option) => option.selected).length;
  }
  return 0;
}

async function fetchDataAndEmbedTemplateInPlaceholder( url, placeholderId, append = false) {
  const response = await fetch(url);
  if (response.ok) {
    const form = await response.json();
    if (append) {
      document.getElementById(placeholderId).innerHTML += form["template"];
    } else {
      document.getElementById(placeholderId).innerHTML = form["template"];
    }
  } else {
    const error = await response.text();
    document.write(error);
  }
}

async function postDataAndEmbedTemplateInPlaceholder(url, placeholderId, body) {
  const token = document.getElementById("csrf_token").value;
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "X-CSRF-TOKEN": token,
    },
    body: JSON.stringify(body),
  });
  if (response.ok) {
    const form = await response.json();
    document.getElementById(placeholderId).innerHTML = form["template"];
  } else {
    const error = await response.text();
    document.write(error);
  }
}

async function deleteDataAndEmbedTemplateInPlaceholder(url, placeholderId) {
  const token = document.getElementById("csrf_token").value;
  const response = await fetch(url, {
    method: "DELETE",
    headers: {
      "X-CSRF-TOKEN": token,
    },
  });
  if (response.ok) {
    const form = await response.json();
    document.getElementById(placeholderId).innerHTML = form["template"];
  } else {
    const error = await response.text();
    document.write(error);
  }
}

function removeInnerHtmlFromPlaceholder(placeholderId) {
  document.getElementById(placeholderId).innerHTML = "";
}

function insertSpinnerInPlaceholder(placeholderId, append = false, spinner = SPINNER) {
  if (append) {
    document.getElementById(placeholderId).innerHTML += spinner;
  } else {
    document.getElementById(placeholderId).innerHTML = spinner;
  }
}

function removeSpinnerInPlaceholder(placeholderId, spinner = SPINNER) {
  const placeholder = document.getElementById(placeholderId);
  placeholder.innerHTML = placeholder.innerHTML.replace(spinner, "");
}

function collectSelection(placeholder) {
  return Array.from(placeholder.children).filter((option) => option.selected).map((option) => {
      return { uuid: option.value,  name: option.innerHTML};
    });
}

function atLeastOneItemIsSelected(placeholder) {
  const selectedItems = Array.from(placeholder.children).filter((option) => option.selected);
  return selectedItems.length > 0;
}

function enableTooltip(elem) {
  return new bootstrap.Tooltip(elem, { trigger: "hover" });
}

/**
 * Enable tooltips everywhere
 * See Bootstrap docs: https://getbootstrap.com/docs/5.0/components/tooltips/#example-enable-tooltips-everywhere
 */

const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
tooltipTriggerList.map(function (tooltipTriggerEl) {return new bootstrap.Tooltip(tooltipTriggerEl, { trigger: "hover" });});

function setNavBarHomeToActive() {
  if (window.location.pathname === "/") {
    document.getElementById("nav-bar-home").setAttribute("class", "nav-link active");
  }
}

function passClickToFileInput() {
  document.getElementById("session-button-upload").click();
}

async function autoUploadSessionFile() {
  const token = document.getElementById("csrf_token").value;
  const selectedFile = document.getElementById("session-button-upload").files[0];
  const submitURL = `${window.location.protocol}//${window.location.host}/session`;
  const formData = new FormData();
  formData.append("file", selectedFile);
  const response = await fetch(submitURL, {
    method: "POST",
    body: formData,
    files: selectedFile,
    headers: {
      "X-CSRF-TOKEN": token,
    },
  });
  if (response.ok) {
    window.location.reload();
  } else {
    const error = await response.text();
    document.write(error);
  }
}

async function deleteCurrentSession() {
  const token = document.getElementById("csrf_token").value;
  const url = `${window.location.protocol}//${window.location.host}/session/`;
  const response = await fetch(url, {
    method: "DELETE",
    headers: {
      "X-CSRF-TOKEN": token,
    },
  });
  if (response.ok) {
    window.location.reload();
  } else {
    const error = await response.text();
    document.write(error);
  }
}

window.addEventListener("load", function () {
  setNavBarHomeToActive();
  document.getElementById("session-button-save").addEventListener("click", passClickToFileInput);
  document.getElementById("session-button-upload").addEventListener("change", autoUploadSessionFile);
  document.getElementById("session-button-clear-confirm").addEventListener("click", deleteCurrentSession);
});