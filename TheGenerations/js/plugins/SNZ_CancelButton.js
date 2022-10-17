 //=============================================================================
// SNZ_CancelButton.js
// Version: 1.0
//----------------------------------------------------------------------------
// by しんぞ
// Released under the MIT license
// http://opensource.org/licenses/mit-license.php
//=============================================================================

/*:
@plugindesc キャンセルボタンを画面上に常設。ノーモア２本指タップ！
@author しんぞ
@help
特にモバイルで「キャンセル」操作がやりづらいため、その対策です。
マップ画面では「メニュー」ボタン、その他では「キャンセル」ボタンが
指定した座標に常時表示されます。
ボタン画像は各自でご用意ください。

戦闘画面でもセーブ画面でも表示されますが、
その代わり、他のウインドウを避けて配置する機能はありません。
（独自のレイヤーを作ってそこにボタンを置いているためです）
他のウインドウやボタンが重ならないように、
別途レイアウト調整プラグインを導入するなどして
チューニングをすると使い勝手が上がると思います。

なお、ボタンは半分のサイズに縮小して設置するようにしてあります。
（高解像度の画面でもきれいに見られるようにです）
そのため、ご用意いただくのは倍のサイズの画像にしてください。
ボタン画像の暗号化には対応していません。
暗号化してデプロイした方は、ボタン画像だけ手作業で
本番ディレクトリに設置してください。

プラグインコマンド
HideCancelButton キャンセルボタンを非表示にします。
ShowCancelButton キャンセルボタンを表示します。

利用規約
ご自由に。クレジットもあってもなくてもいいです。改造改変歓迎。

ところで、納豆のタレって過剰な塩味がおいしいよね。

@param hideswitch
@desc メニューボタンの表示状態を保存しておくスイッチです
@default
@type switch

@param menuurl
@desc メニューボタン画像のファイル
@default btn_menu
@type file
@dir img/system/

@param cancelurl
@desc キャンセルボタン画像のファイル
@default btn_cancel
@type file
@dir img/system/

@param btnx
@desc ボタン画像のX座標　Javascript式が使えます
@default Graphics.boxWidth - 80
@type string

@param btny
@desc ボタン画像のY座標　Javascript式が使えます
@default Graphics.boxHeight - 90
@type string

*/

var Imported = Imported || {};
Imported.SNZ_CancelButton = '1.0';

var SNZ_CancelButton = {};

(function() {
  "use strict";
  var param = new Array();
  var zoom = 0;
  var btnready = false;
  var pressbtn = false;
  var wrapper = document.createElement('div');
  var menubtn = document.createElement('canvas');
  var cancelbtn = document.createElement('canvas');

  //画面の拡大率を算出する関数だよ
  var calcZoom = function() {
    var ww = window.innerWidth;
    var wh = window.innerHeight;
    var cw = Graphics.boxWidth;
    var ch = Graphics.boxHeight;
    return Math.min(ww / cw, wh / ch);
  }

  //-----------------------------------------------------------------------------
  // パラメーターの受け取り

  var pluginName = 'SNZ_CancelButton';
  var _Scene_Base_start = Scene_Base.prototype.start;
  Scene_Base.prototype.start = function() {
    _Scene_Base_start.call(this);

  var paramParse = function(obj) {
      return JSON.parse(JSON.stringify(obj, paramReplace), paramRevive);
  };

  var paramReplace = function(key, value) {
      try {
          return JSON.parse(value || null);
      } catch (e) {
          return value;
      }
  };

  var paramRevive = function(key, value) {
      try {
          return eval(value || value);
      } catch (e) {
          return value;
      }
  };

  var parameters = PluginManager.parameters(pluginName);
  param = paramParse(parameters);

}



  //-----------------------------------------------------------------------------
  // Scene_Base_start

  var Scene_Base_start = Scene_Base.prototype.start;
  Scene_Base.prototype.start = function() {
    Scene_Base_start.call(this);

    zoom = calcZoom();
    window.onresize = function() {
      zoom = calcZoom();
      if (wrapper.id) {
        wrapper.style.transform = 'scale(' + zoom + ')';
      }
    }

    if (!btnready) {
      btnready = true;

      //canvasを用意するよ
      wrapper.id = 'btnarea';
      wrapper.style.position = 'absolute';
      wrapper.style.zIndex = '11';
      wrapper.style.transform = 'scale(' + zoom + ')';
      wrapper.style.width = Graphics.boxWidth + 'px';
      wrapper.style.height = Graphics.boxHeight + 'px';
      wrapper.style.margin = 'auto';
      wrapper.style.left = '0';
      wrapper.style.top = '0';
      wrapper.style.right = '0';
      wrapper.style.bottom = '0';
      menubtn.id = 'menubtn';
      cancelbtn.id = 'cancelbtn';
      menubtn.style.display = cancelbtn.style.display = 'none';
      menubtn.style.position = cancelbtn.style.position = 'absolute';
      menubtn.style.left = cancelbtn.style.left = param.btnx + 'px';
      menubtn.style.top = cancelbtn.style.top = param.btny + 'px';

      //タッチイベントを感知するよ
      var _touchstart = (window.ontouchstart !== undefined) ? 'touchstart' : 'mousedown';
      var _touchend = (window.ontouchend !== undefined) ? 'touchend' : 'mouseup';
      var touchstartfunc = function() {
        Input._currentState['escape'] = true;
        pressbtn = true;
      }
      var touchendfunc = function() {
        Input._currentState['escape'] = false;
        pressbtn = false;
      }

      menubtn.addEventListener(_touchstart, function(e) {
        e.preventDefault();
        touchstartfunc();
      }, false);
      menubtn.addEventListener(_touchend, function() {
        touchendfunc();
      }, false);
      cancelbtn.addEventListener(_touchstart, function(e) {
        e.preventDefault();
        touchstartfunc();
      }, false);
      cancelbtn.addEventListener(_touchend, function() {
        touchendfunc();
      }, false);

      wrapper.appendChild(menubtn);
      wrapper.appendChild(cancelbtn);
      document.body.appendChild(wrapper);

      //ボタンを配置するよ
      var menuimg = new Image();
      var cancelimg = new Image();
      var menuurl = 'img/system/' + param.menuurl + '.png';
      var cancelurl = 'img/system/' + param.cancelurl + '.png';
      menuimg.onerror = function() {
        Graphics.printError('Button Image was Not Found:', menuurl);
      };
      cancelimg.onerror = function() {
        Graphics.printError('Button Image was Not Found:', cancelurl);
      };
      menuimg.src = menuurl;
      cancelimg.src = cancelurl;

      var menuctx = menubtn.getContext('2d');
      menuimg.onload = function() {
        menubtn.width = wrapper.style.width = menuimg.width;
        menubtn.height = wrapper.style.height = menuimg.height;
        menuctx.drawImage(menuimg, 0, 0, menuimg.width, menuimg.height, 0, 0, menuimg.width, menuimg.height);
        menubtn.style.width = menuimg.width / 2  + 'px';
        menubtn.style.height = menuimg.height / 2  + 'px';
      }
      var cancelctx = cancelbtn.getContext('2d');
      cancelimg.onload = function() {
        cancelbtn.width = wrapper.style.width = cancelimg.width;
        cancelbtn.height = wrapper.style.height = cancelimg.height;
        cancelctx.drawImage(cancelimg, 0, 0, cancelimg.width, cancelimg.height, 0, 0, cancelimg.width, cancelimg.height);
        cancelbtn.style.width = menuimg.width / 2  + 'px';
        cancelbtn.style.height = menuimg.height / 2  + 'px';
      }

      Graphics._updateRealScale();
    }
  };


  //-----------------------------------------------------------------------------
  // _Game_Interpreter_pluginCommand

  var _Game_Interpreter_pluginCommand = Game_Interpreter.prototype.pluginCommand;
  Game_Interpreter.prototype.pluginCommand = function(command, args) {
    _Game_Interpreter_pluginCommand.call(this, command, args);
    if (command === 'ShowCancelButton') {
      if($gameSystem._menuEnabled){
        wrapper.style.display = 'block';
        $gameSwitches.setValue(param.hideswitch,false);
      }
    }
    if (command === 'HideCancelButton') {
      wrapper.style.display = 'none';
      $gameSwitches.setValue(param.hideswitch,true);
    }
  };
  //-----------------------------------------------------------------------------
  // _Game_System_prototype_disableMenu
  var _Game_System_prototype_disableMenu = Game_System.prototype.disableMenu;
  Game_System.prototype.disableMenu = function() {
    _Game_System_prototype_disableMenu.call(this);
    wrapper.style.display = 'none';
    $gameSwitches.setValue(param.hideswitch,true);
  };

  var _Game_System_prototype_enableMenu = Game_System.prototype.enableMenu;
  Game_System.prototype.enableMenu = function() {
    _Game_System_prototype_enableMenu.call(this);
    wrapper.style.display = 'block';
    $gameSwitches.setValue(param.hideswitch,false);
  };

  //-----------------------------------------------------------------------------
  // TouchInput_update

  var TouchInput_update = TouchInput.update;
  TouchInput.update = function() {
    if (!pressbtn) {
      TouchInput_update.call(this);
    }
  };
  //-----------------------------------------------------------------------------
  // Scene_Battle_start

  var Scene_Battle_start = Scene_Battle.prototype.start;
  Scene_Battle.prototype.start = function() {
    Scene_Battle_start.call(this);
    wrapper.style.display = 'block';
    menubtn.style.display = 'none';
    cancelbtn.style.display = 'block';
  };

  //-----------------------------------------------------------------------------
  // Scene_Map_start

  var Scene_Map_start = Scene_Map.prototype.start;
  Scene_Map.prototype.start = function() {
    Scene_Map_start.call(this);

    if($gameSwitches.value(param.hideswitch)){
      wrapper.style.display = 'none';
    }
    menubtn.style.display = 'block';
    cancelbtn.style.display = 'none';
  };
  //-----------------------------------------------------------------------------
  // Scene_Map_stop

  var Scene_Map_stop = Scene_Map.prototype.stop;
  Scene_Map.prototype.stop = function() {
    Scene_Map_stop.call(this);

    menubtn.style.display = 'none';
    cancelbtn.style.display = 'block';
  };

})(SNZ_CancelButton);
