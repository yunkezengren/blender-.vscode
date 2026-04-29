// ==UserScript==
// @name     Gitea Document Links
// @description Add buttons to put descriptive links to the current page on the clipboard.
// @version  20
// @match    https://projects.blender.org/*
// @grant    GM.setClipboard
// ==/UserScript==

// Based on: https://projects.blender.org/dr.sybren/.profile/src/branch/main/webbrowser-scripts/gitea-document-links.js

// Remove the 'user/repo:' part of the 'user/repo:branchname' value.
function fix_branchname_copy_button() {
  let header = document.getElementById("pull-desc-display");
  if (!header) return;

  let buttons = header.getElementsByTagName('button');
  if (buttons.length == 0) return;

  let button = buttons[0];
  let text = button.dataset["clipboardText"];
  let textParts = text.split(":");
  textParts.shift();
  let branchName = textParts.join(":");

  button.dataset["clipboardText"] = branchName;
  button.dataset["tooltipContent"] = "Copy branch name \"" + branchName + "\"";
}


function add_document_links() {
  console.log("triggered!");
  let buttons = document.getElementsByClassName("special-greasemonkey-button");
  if (buttons.length > 0) {
    return;
  }

  let url_info = find_url_info();
  let page_name = "";
  let page_title = "";

  if (url_info.issue && url_info.issue != "new") {
    page_name = `#${url_info.issue}`;
    page_title = find_page_title();
  } else if (url_info.pull) {
    page_name = `#${url_info.pull}`;
    page_title = find_page_title();
  } else if (url_info.commit) {
    page_name = `${url_info.commit.substring(0, 12)}`;
    page_title = find_commit_title();
  } else {
    return;
  }

  const url = window.location.href.split("#")[0];

  // Top buttons:
  add_button("MD", `[${page_name}: ${page_title}](${url})`);
  add_button("MD (short)", `[${page_name}](${url})`);
  if (url_info.commit) {
    add_commit_button("MD (log)", page_name, page_title, url);
    add_button("REF", `(${url_info.org}/${url_info.repo}@${url_info.commit})`);
  }
  add_button("TXT", page_name + ": " + page_title);
  if (url_info.pull) {
    add_pr_copy_diff_button("Diff", `https://projects.blender.org/${url_info.org}/${url_info.repo}/pulls/${url_info.pull}.diff`);
  }

  // Buttons at comment area:
  if (url_info.pull) {
    add_comment_button("Build", "@blender-bot build");
    add_comment_button("Package", "@blender-bot package");
  }

}

function add_commit_button(button_title, page_name, page_title, url) {
  const author_elts = document.getElementsByClassName("author");
  if (!author_elts || author_elts.length == 0) {
    console.warn("MD button: Author element not found");
    return;
  }
  const author_elt = author_elts[0];

  const author_links = author_elt.getElementsByTagName("a");
  if (!author_links || author_links.length == 0) {
    console.warn("MD button: Author element has no links:", author_elt);
    return;
  }
  const author_link = author_links[0];
  const author_name = author_link.textContent.trim();

  const author_time_elt = document
    .getElementById("authored-time")
    .getElementsByTagName("relative-time")[0];
  const date = new Date(author_time_elt.getAttribute("datetime"));
  const fmt_date = date.toISOString().split("T")[0];
  add_button(
    button_title,
    `- [${page_name}: ${page_title}](${url}) (*${author_name}*)`
  );
}

function add_header_button(button_text) {
  const button_style = "padding: 0.4rem; border-color: #265787";
  let button = document.createElement("button");
  button.textContent = button_text;
  button.className =
    "ui basic secondary not-in-edit button tiny special-greasemonkey-button";
  button.setAttribute("style", button_style);

  let button_parent_elt = find_button_parent_element();
  if (!button_parent_elt) {
    console.log("no parent elt found");
    return button;
  }

  /* Insert before the 'Edit' button, as otherwise that button doesn't work any more. */
  var sibling = null;
  for (var childNode of button_parent_elt.childNodes) {
    if (
      childNode.className &&
      childNode.className.includes("issue-title-buttons")
    ) {
      sibling = childNode;
      break;
    }
  }
  if (sibling) {
    button_parent_elt.insertBefore(button, sibling);
  } else {
    button_parent_elt.appendChild(button);
  }

  return button;
}

function add_button(button_text, clipboard_text) {
  button = add_header_button(button_text)
  button.setAttribute("title", clipboard_text);
  button.addEventListener("click", function () {
    console.log("Clipboard:", clipboard_text);
    GM.setClipboard(clipboard_text);
  });
}

function add_comment_button(button_text, comment_text) {
  // Find the parent to insert the button into.
  let form = document.getElementById("comment-form");
  if (!form) return;

  let footer = form.getElementsByClassName("field footer")[0];
  if (!footer) return;

  let existing_buttons = footer.getElementsByTagName("button");
  if (existing_buttons.length) {
    footer = existing_buttons[0].parentElement;
  }

  let button = document.createElement("button");
  button.textContent = button_text;
  button.className = "ui secondary button special-greasemonkey-button";
  button.setAttribute("title", comment_text);
  button.addEventListener(
    "click",
    function (event) {
      event.preventDefault();
      event.stopImmediatePropagation();

      console.log("Insert into comment:", comment_text);

      let form = document.getElementById("comment-form");
      if (!form) {
        console.error("cannot find comment form");
        return;
      }

      let textarea = form.getElementsByTagName("textarea")[0];
      if (!textarea) {
        console.error("cannot find text area in form ", form);
        return;
      }

      textarea.value += comment_text + "\n";

      // To trigger Gitea into enabling the 'Comment' button:
      textarea.dispatchEvent(new Event("input"));
    },
    { capture: true }
  );

  footer.insertBefore(button, footer.children[0]);
}

function find_button_parent_element() {
  // For issues & PRs:
  let title_elt = document.getElementById("issue-title-display");
  if (title_elt) {
    // let children = title_elt.getElementsByClassName("edit-button");
    // if (children.length == 0) return undefined;
    // return children[0];
    return title_elt.parentElement;
  }

  // For commits:
  let header_elts = document.getElementsByClassName("ui top commit-header");
  if (header_elts.length > 0) {
    return header_elts[0];
  }
}

function find_page_title() {
  let page_title_elt = document.getElementById("issue-title-display");
  let h1 = page_title_elt.getElementsByTagName("h1")[0];
  let page_title = h1.textContent.trim();
  return page_title.replace(/\s*#\d+$/, "").replace(/\s+/, " ").trim();
}

function find_commit_title() {
  let title_elts = document.getElementsByClassName("commit-summary");
  if (title_elts.length == 0) return "";
  return title_elts[0].getAttribute("title");
}

function find_url_info() {
  let parts = window.location.pathname.split("/");
  let url_info = {
    org: "",
    repo: "",
    issue: "",
    pull: "",
    commit: "",
  };
  // 'parts' will be ["", "$org", "$repo", "$category", "bla"]
  if (parts.length > 1) url_info.org = parts[1];
  if (parts.length > 2) url_info.repo = parts[2];
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
  button = add_top_button(button_text)
  button.setAttribute("title", "Copy diff from: " + diff_url);
  button.addEventListener("click", function () {
    fetch(diff_url, {
        headers: {
          "Accept": "text/plain"
        }
      })
      .then(res => {
        if (!res.ok) {
          console.error("failed to fetch diff");
          return null;
        }
        console.log("Fetched diff");
        return res.text();
      })
      .then(text => {
        if (text) {
          GM.setClipboard(text);
          console.log("Copied diff to clipboard");
        }
      });
  });
}

window.setTimeout(add_document_links, 200);
window.setTimeout(fix_branchname_copy_button, 220);
