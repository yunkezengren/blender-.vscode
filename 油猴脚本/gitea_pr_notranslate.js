// ==UserScript==
// @name     Gitea Issue/PR Notranslate
// @description Mark issue and PR metadata, labels, and diff content as not translatable on projects.blender.org.
// @version  1
// @match    https://projects.blender.org/*
// @run-at   document-start
// ==/UserScript==

"use strict";

const NOTRANSLATE_CLASS = "notranslate";
const APPLY_DELAY_MS = 80;
const LOCATION_POLL_MS = 500;

const STATIC_SELECTORS = [
  "#pull-desc-display",
  ".pull-desc",
  ".pull-desc a",
  ".pull-desc code",
  "#activity-feed .flex-item-main > div",
  "#activity-feed .flex-item-main > div a",
  "#activity-feed .flex-item-main > div relative-time",
  ".flex-item-body",
  ".flex-item-body a",
  ".flex-item-body span",
  ".flex-item-body code",
  ".issue-list .labels .label",
  ".issue-list .ui.label",
  ".issue-card .labels .label",
  ".issue-card .ui.label",
  ".repo-issue-list .labels .label",
  ".repo-issue-list .ui.label",
  ".issue-meta .labels .label",
  ".issue-meta .ui.label",
  ".issue-title-meta .labels .label",
  ".issue-title-meta .ui.label",
  ".diff-stats",
  ".diff-stats-summary",
  ".diff-stat-bar",
  ".diff-detail-box",
  ".diff-detail-stats",
  ".diff-file-box",
  ".diff-file-box .file-header",
  ".diff-file-box .file-header a",
  ".diff-file-box .file-body",
  ".diff-file-box .code-diff",
  ".diff-file-box .code-diff table",
  ".diff-file-box .code-diff td",
  ".diff-file-box .code-diff pre",
  ".diff-file-box .code-diff code",
  ".diff-file-box .file-body pre",
  ".diff-file-box .file-body code",
  ".diff-file-box .lines-num",
  ".diff-file-box .lines-code",
  ".diff-file-box .file-info",
  ".diff-file-box .file-info a",
  ".diff-file-box .file-path",
  ".diff-file-box .file-title-name",
  ".diff-file-box .blob-excerpt",
  ".pull-files .file-header",
  ".pull-files .file-body",
  ".pull-files pre",
  ".pull-files code",
  ".issue-content-right .ui.label",
  ".issue-content-right .ui.labels .label",
  ".issue-content-right .label",
  ".issue-content-right .labels",
  ".issue-sidebar .ui.label",
  ".issue-sidebar .ui.labels .label",
  ".issue-sidebar .label",
  ".issue-sidebar .labels",
  ".ui.label",
  ".labels .label",
];

let scheduled = false;
let last_location = "";

function is_target_page() {
  const parts = window.location.pathname.split("/");
  if (parts.length > 1 && (parts[1] === "issues" || parts[1] === "pulls")) {
    return true;
  }

  if (parts.length > 3 && parts[3] === "issues") {
    return true;
  }

  if (parts.length > 3 && parts[3] === "pulls") {
    if (parts.length > 4 && parts[4] === "new") {
      return false;
    }

    return true;
  }

  return false;
}

function mark_notranslate(node) {
  if (!(node instanceof HTMLElement)) {
    return;
  }

  node.setAttribute("translate", "no");
  node.classList.add(NOTRANSLATE_CLASS);

  if (!node.lang) {
    node.lang = "en";
  }
}

function mark_selector_matches(root, selector) {
  if (root instanceof HTMLElement && root.matches(selector)) {
    mark_notranslate(root);
  }

  for (const node of root.querySelectorAll(selector)) {
    mark_notranslate(node);
  }
}

function mark_label_nodes(root) {
  const label_nodes = root.querySelectorAll(".ui.label, .labels .label, .label");
  for (const node of label_nodes) {
    mark_notranslate(node);

    for (const child of node.querySelectorAll("span, a, strong, em, b")) {
      mark_notranslate(child);
    }
  }
}

function mark_flex_item_bodies(root) {
  const bodies = root.querySelectorAll(".flex-item-body");
  for (const body of bodies) {
    mark_notranslate(body);
    for (const child of body.querySelectorAll("*")) {
      mark_notranslate(child);
    }
  }
}

function mark_text_patterns(root) {
  const text_nodes = root.querySelectorAll("div, span, a, strong, code");
  for (const node of text_nodes) {
    const text = node.textContent?.trim() || "";
    if (!text) {
      continue;
    }

    if (/^[+-]\d+\s+[+-]\d+$/.test(text)) {
      mark_notranslate(node);
      mark_notranslate(node.parentElement);
      continue;
    }

    if (/^[A-Za-z0-9_.\-\/]+$/.test(text) && text.includes("/")) {
      mark_notranslate(node);
      continue;
    }

    if (text.includes("@@") && text.length < 80) {
      mark_notranslate(node);
      continue;
    }

    if (is_metadata_label_text(text)) {
      mark_notranslate(node);
      mark_notranslate(node.parentElement);
      mark_notranslate(node.closest(".ui.label, .label, .labels, .ui.labels"));
    }
  }
}

function is_metadata_label_text(text) {
  const normalized_text = text.replace(/\s+/g, " ").trim();
  return [
    "Severity",
    "Normal",
    "Status",
    "Needs Triage",
    "Type",
    "Bug",
    "Priority",
    "Module",
    "Platform",
    "Branch",
    "Review",
    "Labels",
  ].includes(normalized_text);
}

function apply_notranslate(root = document) {
  if (!is_target_page()) {
    return;
  }

  for (const selector of STATIC_SELECTORS) {
    mark_selector_matches(root, selector);
  }

  mark_flex_item_bodies(root);
  mark_label_nodes(root);
  mark_text_patterns(root);
}

function schedule_apply() {
  if (scheduled) {
    return;
  }

  scheduled = true;
  window.setTimeout(() => {
    scheduled = false;
    apply_notranslate(document);
  }, APPLY_DELAY_MS);
}

function install_observer() {
  const observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      if (mutation.type === "childList" && mutation.addedNodes.length > 0) {
        schedule_apply();
        return;
      }
    }
  });

  observer.observe(document.documentElement, {
    childList: true,
    subtree: true,
  });
}

function install_location_watcher() {
  last_location = window.location.href;
  window.setInterval(() => {
    if (window.location.href === last_location) {
      return;
    }

    last_location = window.location.href;
    schedule_apply();
  }, LOCATION_POLL_MS);
}

function main() {
  schedule_apply();
  install_observer();
  install_location_watcher();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", main, { once: true });
}
else {
  main();
}
