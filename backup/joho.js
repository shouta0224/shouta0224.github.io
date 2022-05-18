const information=document.getElementById("information");
const infoArray=[];

// 位置情報取得成功時の処理
let successCallback=(position)=>{
  information.innerHTML="";

  infoArray.緯度=position.coords.latitude;
  infoArray.経度=position.coords.longitude;
  infoArray.高度=position.coords.altitude;
  infoArray.緯度と経度の誤差=position.coords.accuracy;
  infoArray.高度の誤差=position.coords.altitudeAccuracy;
  infoArray.方角=position.coords.heading;
  infoArray.速度=position.coords.speed;

  for(key in infoArray){
    information.innerHTML+=(key+":"+infoArray[key]+"<br>");
  }

}

// 位置情報取得失敗時の処理
const failureCallback=(error)=>{
  let errorMessage = "";
    switch(error.code){
      case 1:
        errorMessage = "位置情報の取得がユーザーに拒否されました";
        break;
      case 2:
        errorMessage = "位置情報が判定できません";
        break;
      case 3:
        errorMessage = "位置情報の取得処理がタイムアウトしました";
        break;
      }
    information.innerHTML=errorMessage;
}

//ユーザーの現在の位置情報を取得を実行
navigator.geolocation.watchPosition(successCallback, failureCallback);