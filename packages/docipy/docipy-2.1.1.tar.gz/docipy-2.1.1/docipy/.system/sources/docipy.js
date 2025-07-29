const menu = document.querySelector("body>span");
const body = document.querySelector("body");
const header = document.querySelector("header");
const nav = document.querySelector("header>nav");
const ptags = document.querySelectorAll("header p");
const atags = document.querySelectorAll("header a");
const hint = document.querySelector("header>a>hint");
const nava = document.querySelectorAll("nav>a");
const code = document.querySelectorAll(".docipygroup>section pre>code");
const searchIN = document.querySelector("header>div>input");
const searchBT = document.querySelector("header>div>i");
const searchGR = document.querySelectorAll(".docipygroup section");
const vers = document.querySelector("#version");
const version = document.querySelector("#version span");
const versions = document.querySelector("#version ul");
const versionsN = document.querySelectorAll("#version ul li");

if (versionsN.length == 0) {
  version.classList.remove("bi-chevron-down");
}

function addre(parent = null, query = "", name = "", remove = false) {
  if (!parent || !query || !name) {
    return false;
  }

  var items = parent.querySelectorAll(query);
  if (!items) {
    return false;
  }

  items.forEach((item) => {
    if (remove) {
      item.classList.remove(name);
    } else {
      item.classList.add(name);
    }
  });

  return true;
}

function load() {
  var hash = window.location.hash.replaceAll("#", "");
  if (!hash) {
    return false;
  }

  let lists = document.querySelectorAll("header ul");
  if (lists) {
    lists.forEach((i) => {
      i.classList.add("hide");
    });
  }

  var items = hash.split("-");
  var build = [];
  var actives = document.querySelectorAll("header .active");
  actives.forEach((x) => {
    x.classList.remove("active");
  });

  var blocks = document.querySelectorAll(".docipygroup, .docipy-docipyblock");
  items.forEach((x) => {
    build.push(x);
    let item = build.join("-");
    let label = document.querySelector(`.${item}`);
    let list = document.querySelector(`.${item}-docipymenu`);
    let block = document.querySelector(`.${item}-docipyblock`);
    if (label) {
      label.classList.add("active");
    }
    if (list) {
      list.classList.remove("hide");
    }
    if (block) {
      if (blocks) {
        blocks.forEach((i) => {
          let detect = i.querySelector(`.${item}-docipyblock`);
          if (!detect) {
            i.classList.add("hide");
          }
        });
      }

      block.classList.remove("hide");
      addre(document, ".docipygroup section", "hide");
      addre(block, ".docipygroup section", "hide", true);

      let hashset = window.location.hash.replaceAll("#", "");
      let sections = block.parentElement.querySelector(`.${item}-docipyblock>section`);
      let find = block.querySelector(`.${hashset}-docipyblock`);
      let tagset = document.querySelector(`.${hashset}`);
      if (!sections && !find && tagset && tagset.tagName == "P") {
        let first = block.querySelector("section").id;
        if (first) {
          window.location.hash = first;
          if (body.style.overflowY == "hidden") {
            menu.click();
          }
        }
      }
    }
    if (label) {
      hint.textContent = label.textContent;
    } else {
      hint.textContent = "Home";
    }
  });
}

menu.addEventListener("click", function (event) {
  event.preventDefault();
  if (this.classList.contains("bi-list")) {
    body.style.overflowY = "hidden";
    header.style.height = "100%";
    nav.style.display = "flex";
    this.classList.remove("bi-list");
    this.classList.add("bi-x-lg");
  } else {
    body.style.overflowY = "auto";
    header.style.height = "auto";
    nav.style.display = "none";
    this.classList.remove("bi-x-lg");
    this.classList.add("bi-list");
  }
});

window.addEventListener("hashchange", function () {
  load();
});

load();

atags.forEach((link) => {
  link.addEventListener("click", function (event) {
    if (body.style.overflowY == "hidden") {
      menu.click();
    }
  });
});

nava.forEach((item) => {
  item.addEventListener("click", function (event) {
    event.preventDefault();
    let href = item.getAttribute("href").replaceAll("#", "");
    if (item.classList.contains("active")) {
      window.location.hash = "docipy";
    } else {
      window.location.hash = href;
    }
  });
});

ptags.forEach((link) => {
  link.addEventListener("click", function (event) {
    event.preventDefault();
    let item = event.target.closest("p");
    let href = item.getAttribute("ref");
    if (item.classList.contains("active")) {
      let uls = item.querySelectorAll("ul");
      if (uls) {
        uls.forEach((i) => {
          i.classList.add("hide");
        });
        let next = item.nextElementSibling;
        if (next.tagName == "UL") {
          next.classList.add("hide");
        }
        item.classList.remove("active");
        if (item.classList.contains("bi")) {
          window.location.hash = "docipy";
        }
        return true;
      }
    }
    if (href) {
      let next = item.nextElementSibling;
      if (next && next.tagName == "UL") {
        item.classList.add("active");
        next.classList.remove("hide");
      } else if (body.style.overflowY == "hidden") {
        menu.click();
      }
      window.location.hash = href;
    }
  });
});

code.forEach((x) => {
  x.insertAdjacentHTML("beforebegin", '<copy class="bi bi-clipboard" onclick="docipycopycode(this);"></copy>');
});

function docipycopycode(element) {
  var code = element.nextElementSibling;
  if (code.tagName != "CODE") {
    return false;
  }

  let range = document.createRange();
  range.selectNode(code);

  let selection = window.getSelection();
  selection.removeAllRanges();
  selection.addRange(range);

  document.execCommand("copy");
  selection.removeAllRanges();
  element.classList.remove("bi-clipboard");
  element.classList.add("bi-clipboard-check");

  setTimeout(function () {
    element.classList.remove("bi-clipboard-check");
    element.classList.add("bi-clipboard");
  }, 2000);
}

function toCapitalCaseAll(str) {
  return str
    .split(" ")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()) // Capitalize the first letter of each word and lowercase the rest
    .join(" ");
}

function toCapitalCase(str) {
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

function searchMark(section = null, text = "", label = "", unmark = false, iterate = true) {
  if (!section && !label) {
    return false;
  }

  var hint = label.tagName == "P" ? "ref" : "href";
  var buil = [];
  var parts = label.getAttribute(hint).replaceAll("#", "").split("-");
  if (iterate && parts) {
    parts.forEach((x) => {
      buil.push(x);
      let item = document.querySelector(`header nav .${buil.join("-")}`);
      if (item) {
        searchMark(section, text, item, unmark, false);
      }
    });
  }

  let html = section.innerHTML;
  let marked = html.includes(`<docipyhighlightstring>${text}</docipyhighlightstring>`);

  if (!iterate) {
    html = html.replaceAll("<docipyhighlightstring>", "").replaceAll("</docipyhighlightstring>", "");
  }

  if (unmark) {
    label.classList.remove("docipyhighlight");
    section.innerHTML = html;
  } else {
    label.classList.add("docipyhighlight");
    if (!iterate && !marked) {
      section.innerHTML = html
        .replaceAll(text.toUpperCase(), `<docipyhighlightstring>${text.toUpperCase()}</docipyhighlightstring>`)
        .replaceAll(toCapitalCase(text), `<docipyhighlightstring>${toCapitalCase(text)}</docipyhighlightstring>`)
        .replaceAll(toCapitalCaseAll(text), `<docipyhighlightstring>${toCapitalCaseAll(text)}</docipyhighlightstring>`)
        .replaceAll(text.toLowerCase(), `<docipyhighlightstring>${text.toLowerCase()}</docipyhighlightstring>`)
        .replaceAll(text, `<docipyhighlightstring>${text}</docipyhighlightstring>`);
    }
  }
}

searchBT.addEventListener("click", function (e) {
  var text = searchIN.value.toLowerCase().trim();
  let lbl = document.querySelectorAll("header nav .docipyhighlight");
  if (lbl) {
    lbl.forEach((l) => {
      l.classList.remove("docipyhighlight");
    });
  }
  if (!text) {
    let all = document.querySelectorAll(".docipygroup>section");
    if (all) {
      all.forEach((m) => {
        m.innerHTML = m.innerHTML.replaceAll("<docipyhighlightstring>", "").replaceAll("</docipyhighlightstring>", "");
      });
    }
    return true;
  }

  var detcted = false;
  searchGR.forEach((section) => {
    var divText = section.textContent.toLowerCase();
    let name = `header nav .${section.id}`;
    let label = document.querySelector(name);
    if (!label) {
      return false;
    }
    if (text !== "" && divText.includes(text)) {
      searchMark(section, searchIN.value, label);
      detcted = true;
    } else {
      searchMark(section, text, label, true, false);
    }
  });

  if (detcted && window.innerWidth < 1040) {
    menu.click();
  }
});

searchIN.addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    searchBT.click();
  }
});

version.addEventListener("click", function (e) {
  if (versionsN.length == 0) return false;
  if (vers.classList.contains("versions-open")) {
    this.classList.add("bi-chevron-down");
    this.classList.remove("bi-chevron-up");
    vers.classList.remove("versions-open");
  } else {
    this.classList.remove("bi-chevron-down");
    this.classList.add("bi-chevron-up");
    vers.classList.add("versions-open");
  }
});

versionsN.forEach((x) => {
  x.addEventListener("click", function (e) {
    var number = this.textContent.replaceAll("v", "").trim();
    var hash = window.location.hash;
    var base = "";
    var href = window.location.href;
    let protocol = window.location.protocol;
    let sufix = protocol == "file:" ? ".html" : "";
    if (this.classList.contains("latest-version")) {
      let v = version.textContent.replace("v", "").trim();
      let prefix = protocol == "file:" ? "/index.html" : "";
      href = href.replace(`/version/${v}${sufix}`, `${prefix}`);
      window.location.href = href.replace(`/version/${v}${sufix}`, `${prefix}`);
      return true;
    }

    if (href.includes("/version/")) base = href.split("/version/")[0] + "/";
    if (number) {
      href = `${base}version/${number}${sufix}${hash}`;
      window.location.href = `${base}version/${number}${sufix}${hash}`;
      return true;
    }
  });
});

document.addEventListener("click", function (event) {
  if (!vers.contains(event.target) && vers.classList.contains("versions-open")) {
    version.click();
  }
});
