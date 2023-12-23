var character = document.getElementById("character");
var block = document.getElementById("block");
var game = document.getElementById("game");
var score = 0;

document.addEventListener("keydown", function(event) {
  if (event.keyCode == 32) {
    if (character.classList == "animate") {
      return;
    }
    character.classList.add("animate");
    setTimeout(function() {
      character.classList.remove("animate");
    }, 500);
  }
});

var checkDead = setInterval(function() {
  var characterTop = parseInt(window.getComputedStyle(character).getPropertyValue("top"));
  var blockLeft = parseInt(window.getComputedStyle(block).getPropertyValue("left"));
  if (blockLeft < 20 && blockLeft > 0 && characterTop >= 130) {
    block.style.animation = "none";
    block.style.display = "none";
    alert("ゲームオーバー！スコア: " + score);
  } else {
    score++;
  }
}, 10);
