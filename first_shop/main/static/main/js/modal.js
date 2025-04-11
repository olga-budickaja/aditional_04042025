const buttons = document.querySelectorAll(".content_page .btn, .product .btn");

buttons.forEach((button) => {
  button.addEventListener("click", (event) => {
    const bg = document.querySelector(".bg");
    bg.classList.add("active");
  });
});

const close_btn = document.querySelector(".modal .btn");

close_btn.addEventListener("click", (event) => {
  const bg = document.querySelector(".bg");
  bg.classList.remove("active");
});
