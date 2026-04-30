// ==UserScript==
// @name     Gitea Document Links
// @description Add polished shortcut buttons for copying links and common PR comments.
// @version  21
// @match    https://projects.blender.org/*
// @grant    GM.setClipboard
// ==/UserScript==

// Based on: https://projects.blender.org/dr.sybren/.profile/src/branch/main/webbrowser-scripts/gitea-document-links.js

"use strict";

const SITE_ROOT = "https://projects.blender.org";
const HEADER_BUTTON_CLASS = "special-greasemonkey-button";
const HEADER_TOOLBAR_CLASS = "special-greasemonkey-toolbar";
const COMMENT_TOOLBAR_CLASS = "special-greasemonkey-comment-toolbar";
const STYLE_ELEMENT_ID = "special-greasemonkey-toolbar-style";
const BUTTON_FEEDBACK_MS = 1200;
const CONFIG = {
  comment_buttons: {
    build: false,
    package: false,
  },
  theme: {
    toolbar_gap: "0.35rem",
    toolbar_margin: "0 0.5rem 0.35rem 0",
    comment_toolbar_margin: "0 0 0.5rem",
    button_padding: "0.28rem 0.65rem",
    button_radius: "7px",
    button_border: "#7f8b9d",
    button_bg_start: "#f7f9fb",
    button_bg_end: "#eef2f6",
    button_text: "#4e5c70",
    button_shadow: "0 1px 2px rgba(17, 24, 39, 0.08)",
    button_hover_border: "#6f7b8d",
    button_hover_bg_start: "#fbfcfd",
    button_hover_bg_end: "#eef1f5",
    button_hover_shadow: "0 2px 6px rgba(17, 24, 39, 0.10)",
    button_font_size: "12px",
    button_font_weight: "600",
  },
};

// Remove the "user/repo:" part of the "user/repo:branchname" value.
function fix_branchname_copy_button() {
  const header = document.getElementById("pull-desc-display");
  if (!header) {
    return;
  }

  const button = header.getElementsByTagName("button")[0];
  const text = button?.dataset?.clipboardText;
  if (!text || !text.includes(":")) {
    return;
  }

  const branch_name = text.split(":").slice(1).join(":");
  button.dataset.clipboardText = branch_name;
  button.dataset.tooltipContent = `Copy branch name "${branch_name}"`;
}

function add_document_links() {
  ensure_styles();

  if (document.querySelector(`.${HEADER_BUTTON_CLASS}`)) {
    return;
  }

  const url_info = find_url_info();
  const page_info = find_page_info(url_info);
  if (!page_info) {
    return;
  }

  const url = window.location.href.split("#")[0];

  add_clipboard_button("MD", `[${page_info.name}: ${page_info.title}](${url})`);
  add_clipboard_button("MD Short", `[${page_info.name}](${url})`);
  add_clipboard_button("Text", `${page_info.name}: ${page_info.title}`);

  if (url_info.commit) {
    add_commit_button("MD Log", page_info, url);
    add_clipboard_button("Ref", `(${url_info.org}/${url_info.repo}@${url_info.commit})`);
  }

  if (url_info.pull) {
    add_pr_copy_diff_button(
      "Diff",
      `${SITE_ROOT}/${url_info.org}/${url_info.repo}/pulls/${url_info.pull}.diff`
    );
    if (CONFIG.comment_buttons.build) {
      add_comment_button("Build", "@blender-bot build");
    }
    if (CONFIG.comment_buttons.package) {
      add_comment_button("Package", "@blender-bot package");
    }
  }
}

function ensure_styles() {
  if (document.getElementById(STYLE_ELEMENT_ID)) {
    return;
  }

  const style = document.createElement("style");
  style.id = STYLE_ELEMENT_ID;
  const theme = CONFIG.theme;
  style.textContent = `
    .${HEADER_TOOLBAR_CLASS} {
      display: flex;
      flex-wrap: wrap;
      gap: ${theme.toolbar_gap};
      align-items: center;
      margin: ${theme.toolbar_margin};
    }

    .${COMMENT_TOOLBAR_CLASS} {
      display: flex;
      flex-wrap: wrap;
      gap: ${theme.toolbar_gap};
      align-items: center;
      margin: ${theme.comment_toolbar_margin};
    }

    .${HEADER_BUTTON_CLASS} {
      appearance: none;
      border: 1px solid ${theme.button_border};
      border-radius: ${theme.button_radius};
      background: linear-gradient(180deg, ${theme.button_bg_start} 0%, ${theme.button_bg_end} 100%);
      color: ${theme.button_text};
      box-shadow: ${theme.button_shadow};
      font-size: ${theme.button_font_size};
      font-weight: ${theme.button_font_weight};
      letter-spacing: 0.01em;
      padding: ${theme.button_padding};
      line-height: 1.2;
      transition:
        transform 0.14s ease,
        box-shadow 0.14s ease,
        border-color 0.14s ease,
        background 0.14s ease;
    }

    .${HEADER_BUTTON_CLASS}:hover {
      background: linear-gradient(180deg, ${theme.button_hover_bg_start} 0%, ${theme.button_hover_bg_end} 100%);
      border-color: ${theme.button_hover_border};
      box-shadow: ${theme.button_hover_shadow};
      transform: translateY(-1px);
    }

    .${HEADER_BUTTON_CLASS}:active {
      transform: translateY(0);
      box-shadow: 0 2px 6px rgba(16, 45, 74, 0.16);
    }

    .${HEADER_BUTTON_CLASS}:disabled {
      cursor: wait;
      opacity: 0.78;
      transform: none;
      box-shadow: none;
    }
  `;
  document.head.appendChild(style);
}

function add_commit_button(button_text, page_info, url) {
  const author_name = find_commit_author_name();
  if (!author_name) {
    console.warn("MD Log button: author link not found");
    return;
  }

  add_clipboard_button(
    button_text,
    `- [${page_info.name}: ${page_info.title}](${url}) (*${author_name}*)`
  );
}

function find_commit_author_name() {
  const author_elt = document.getElementsByClassName("author")[0];
  const author_link = author_elt?.getElementsByTagName("a")[0];
  return author_link?.textContent?.trim() || "";
}

function ensure_header_button_toolbar() {
  const button_parent_elt = find_button_parent_element();
  if (!button_parent_elt) {
    console.warn("Document links: no header parent element found");
    return null;
  }

  let toolbar = button_parent_elt.querySelector(`.${HEADER_TOOLBAR_CLASS}`);
  if (toolbar) {
    return toolbar;
  }

  toolbar = document.createElement("div");
  toolbar.className = HEADER_TOOLBAR_CLASS;

  let sibling = null;
  for (const child_node of button_parent_elt.childNodes) {
    if (
      child_node.className &&
      child_node.className.includes("issue-title-buttons")
    ) {
      sibling = child_node;
      break;
    }
  }

  if (sibling) {
    button_parent_elt.insertBefore(toolbar, sibling);
  }
  else {
    button_parent_elt.appendChild(toolbar);
  }

  return toolbar;
}

function create_button(button_text, title, on_click) {
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = button_text;
  button.dataset.defaultLabel = button_text;
  button.className = HEADER_BUTTON_CLASS;
  button.title = title;
  button.addEventListener("click", async (event) => {
    event.preventDefault();
    await on_click(button, event);
  });
  return button;
}

function add_clipboard_button(button_text, clipboard_text) {
  const toolbar = ensure_header_button_toolbar();
  if (!toolbar) {
    return;
  }

  const button = create_button(button_text, clipboard_text, async (button_elt) => {
    GM.setClipboard(clipboard_text);
    flash_button_state(button_elt, "Copied");
  });
  toolbar.appendChild(button);
}

function add_comment_button(button_text, comment_text) {
  const toolbar = ensure_comment_button_toolbar();
  if (!toolbar) {
    return;
  }

  const button = create_button(button_text, comment_text, async (button_elt, event) => {
    event.stopImmediatePropagation();

    const textarea = document
      .getElementById("comment-form")
      ?.getElementsByTagName("textarea")[0];
    if (!textarea) {
      console.error("Document links: cannot find comment textarea");
      flash_button_state(button_elt, "Missing");
      return;
    }

    textarea.value = append_comment_line(textarea.value, comment_text);
    textarea.dispatchEvent(new Event("input", { bubbles: true }));
    flash_button_state(button_elt, "Inserted");
  });

  toolbar.appendChild(button);
}

function ensure_comment_button_toolbar() {
  const form = document.getElementById("comment-form");
  const footer = form?.getElementsByClassName("field footer")[0];
  if (!footer) {
    return null;
  }

  let button_host = footer;
  const existing_button = footer.getElementsByTagName("button")[0];
  if (existing_button?.parentElement) {
    button_host = existing_button.parentElement;
  }

  let toolbar = button_host.querySelector(`.${COMMENT_TOOLBAR_CLASS}`);
  if (toolbar) {
    return toolbar;
  }

  toolbar = document.createElement("div");
  toolbar.className = COMMENT_TOOLBAR_CLASS;
  button_host.insertBefore(toolbar, button_host.firstChild);
  return toolbar;
}

function append_comment_line(current_text, comment_text) {
  if (!current_text) {
    return `${comment_text}\n`;
  }

  const suffix = current_text.endsWith("\n") ? "" : "\n";
  return `${current_text}${suffix}${comment_text}\n`;
}

function find_button_parent_element() {
  const title_elt = document.getElementById("issue-title-display");
  if (title_elt) {
    return title_elt.parentElement;
  }

  const header_elts = document.getElementsByClassName("ui top commit-header");
  if (header_elts.length > 0) {
    return header_elts[0];
  }

  return null;
}

function find_page_title() {
  const page_title_elt = document.getElementById("issue-title-display");
  const h1 = page_title_elt?.getElementsByTagName("h1")[0];
  const page_title = h1?.textContent?.trim() || "";
  return page_title.replace(/\s*#\d+$/, "").replace(/\s+/g, " ").trim();
}

function find_commit_title() {
  const title_elt = document.getElementsByClassName("commit-summary")[0];
  return title_elt?.getAttribute("title") || title_elt?.textContent?.trim() || "";
}

function find_page_info(url_info) {
  if (url_info.issue && url_info.issue !== "new") {
    return {
      name: `#${url_info.issue}`,
      title: find_page_title(),
    };
  }

  if (url_info.pull) {
    return {
      name: `#${url_info.pull}`,
      title: find_page_title(),
    };
  }

  if (url_info.commit) {
    return {
      name: url_info.commit.substring(0, 12),
      title: find_commit_title(),
    };
  }

  return null;
}

function find_url_info() {
  const parts = window.location.pathname.split("/");
  const url_info = {
    org: "",
    repo: "",
    issue: "",
    pull: "",
    commit: "",
  };

  // "parts" will be ["", "$org", "$repo", "$category", "bla"].
  if (parts.length > 1) {
    url_info.org = parts[1];
  }
  if (parts.length > 2) {
    url_info.repo = parts[2];
  }
  if (parts.length > 4) {
    switch (parts[3]) {
      case "issues":
        url_info.issue = parts[4];
        break;
      case "pulls":
        url_info.pull = parts[4];
        break;
      case "commit":
        url_info.commit = parts[4];
        break;
    }
  }

  return url_info;
}

function add_pr_copy_diff_button(button_text, diff_url) {
  const toolbar = ensure_header_button_toolbar();
  if (!toolbar) {
    return;
  }

  const button = create_button(button_text, `Copy diff from ${diff_url}`, async (button_elt) => {
    set_button_loading(button_elt, "Loading");

    try {
      const response = await fetch(diff_url, {
        headers: {
          Accept: "text/plain",
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch diff: ${response.status}`);
      }

      const diff_text = await response.text();
      GM.setClipboard(diff_text);
      flash_button_state(button_elt, "Copied");
    }
    catch (error) {
      console.error("Document links: failed to copy diff", error);
      flash_button_state(button_elt, "Failed");
    }
  });

  toolbar.appendChild(button);
}

function set_button_loading(button, label) {
  clear_button_feedback(button);
  button.disabled = true;
  button.textContent = label;
}

function flash_button_state(button, label) {
  clear_button_feedback(button);
  button.disabled = false;
  button.textContent = label;
  button._feedbackTimer = window.setTimeout(() => {
    button.textContent = button.dataset.defaultLabel;
  }, BUTTON_FEEDBACK_MS);
}

function clear_button_feedback(button) {
  if (button._feedbackTimer) {
    window.clearTimeout(button._feedbackTimer);
    button._feedbackTimer = null;
  }
}

window.setTimeout(add_document_links, 200);
window.setTimeout(fix_branchname_copy_button, 220);
