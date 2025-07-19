const menuOpenSvg = document.querySelector("#menu-open-svg");
const menuCloseSvg = document.querySelector("#menu-close-svg");
const menuBtn = document.querySelector("#menu-btn");
const mobileMenu = document.querySelector("#mobile-menu");

menuBtn.addEventListener("click", () => {
  if (menuBtn.classList.contains("close")) {
    menuBtn.classList.remove("close");
    menuOpenSvg.classList.replace("hidden", "block");
    menuCloseSvg.classList.replace("block", "hidden");
    mobileMenu.classList.replace("hidden", "block");
  } else {
    menuBtn.classList.add("close");
    menuOpenSvg.classList.replace("block", "hidden");
    menuCloseSvg.classList.replace("hidden", "block");
    mobileMenu.classList.replace("block", "hidden");
  }
});
