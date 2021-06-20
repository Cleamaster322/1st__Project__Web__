const wrapper = document.querySelector(".followers_search_block"),
      textInput = document.querySelector(".followers_search_block > input[type='text']");

textInput.addEventListener("keyup", event => {
  wrapper.setAttribute("data-text", event.target.value);
});


function delUser() {
  var elem = document.getElementById("delete_follower");
  var color = window.getComputedStyle(elem).getPropertyValue("color");
  var back = window.getComputedStyle(elem).getPropertyValue("background");
  var back_hover = window.getComputedStyle(elem.hover).getPropertyValue("background");
  var change = document.getElementById("delete_follower");
  var color1 = '#ED4956';
  var color2 = '#4ACFFF';
  if (change.innerHTML == "Заблокировать")
  {
    change.innerHTML = "Разблокировать";
    color.color = color2;
    back.background = color2;
    back_hover.background = color2;
  }
  else {
    change.innerHTML = "Заблокировать";
    color.color = color1;
    back.background = color1;
    back_hover.background = color1;
  }
}
// Осталось реализовать изменение цвета при нажатии на кнопку и прикрутить к ней стили