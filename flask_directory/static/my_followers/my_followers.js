const wrapper = document.querySelector(".followers_search_block"),
      textInput = document.querySelector(".followers_search_block > input[type='text']");

textInput.addEventListener("keyup", event => {
  wrapper.setAttribute("data-text", event.target.value);
});


function delUser() {
  var change = document.getElementById("delete_follower");
  var color1 = '#ED4956';
  var color2 = '#E3D802';
  if (change.innerHTML == "Заблокировать")
  {
    change.innerHTML = "Разблокировать";
  }
  else {
    change.innerHTML = "Заблокировать";
  }
}
// Осталось реализовать изменение цвета при нажатии на кнопку и прикрутить к ней стили