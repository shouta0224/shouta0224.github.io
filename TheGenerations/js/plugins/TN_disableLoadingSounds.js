//=============================================================================
// TN_disableLoadingSounds.js
// Version: 1.00
// ----------------------------------------------------------------------------
// terunon
// https://twitter.com/trinitroterunon
//=============================================================================

/*:
 * @plugindesc オプションでBGM音量などを0%にした際、
 * 読み込み自体を行わないようにして通信負荷を減らします。
 * @author terunon
 *
 * @help
 * オプションで0%に設定したBGM,BGS,SE,MEを、
 * 再生しないだけでなく、読み込まないようにして余計な通信を減らします。
 * 仕様として、BGMが0%に設定されたことで無視された場合、
 * 値を0%以外に戻しても、次回のBGM再生判定までBGMは開始されません。
 * 
 * Copyright (c) 2016 terunon (AliasAche)
 * クレジットとして、「terunon（エイリアスエイク）」を、
 * ReadMeまたはブラウザ等の視認できる場所に記載していただければ、
 * 営利非営利問わず、あらゆるツクールMV作品で使用・改変いただけます。
 *
 * ※素材の利用を、まるで制作スタッフの一人のように見せるクレジット表記は、
 *   無用なトラブルの元になるので何卒お控えください。
 *
 * 制作応援しています。 terunon
 */

(function() {
'use strict';

var TN_AudioManager_playBgm = AudioManager.playBgm;
AudioManager.playBgm = function(bgm, pos) {
    if (AudioManager._bgmVolume == 0) return;
    TN_AudioManager_playBgm.call(this, bgm, pos);
};

var TN_AudioManager_playBgs = AudioManager.playBgs;
AudioManager.playBgs = function(bgs, pos) {
    if (AudioManager._bgsVolume == 0) return;
    TN_AudioManager_playBgs.call(this, bgs, pos);
};

var TN_AudioManager_playMe = AudioManager.playMe;
AudioManager.playMe = function(me, pos) {
    if (AudioManager._meVolume == 0) return;
    TN_AudioManager_playMe.call(this, me, pos);
};

var TN_AudioManager_playSe = AudioManager.playSe;
AudioManager.playSe = function(se, pos) {
    if (AudioManager._seVolume == 0) return;
    TN_AudioManager_playSe.call(this, se, pos);
};
})();
