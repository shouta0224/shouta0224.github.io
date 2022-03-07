<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>しょうたのサイト</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
    <link rel="stylesheet" href="form.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW" crossorigin="anonymous"></script>
</head>
<body dada-lait-site="white">
    <a href="index.html"><img src="logo.png" alt="ロゴ"></a><a href="videos.html" style="color: gray;text-decoration: none;" rel="nofollow" class="btn btn-outline-secondary">Youtube動画集　</a><a href="links.html" style="color: gray;text-decoration: none;" rel="nofollow" class="btn btn-outline-secondary">リンク集</a>
    <form action="send.php" method="post">
        <p class="lead-form">フォーム!</p>

        <div class="item">
            <label class="label">ニックネーム：</label>
            <input class="inputs" type="text" name="yourname" value="<?php echo $_POST['yourname']; ?>" disabled>
        </div>

        <div class="item">
            <label class="label">コメント</label>
            <textarea class="inputs" name="comment" value="<?php echo $_POST['comment']; ?>" disabled></textarea>
        </div>

        <div class="item">
            <p class="label">エディション</p>
            <select class="inputs" name="edi" value="<?php echo $_POST['edi']; ?>" disabled>
            <option value="java">Java版</option>
            <option value="bedrock">統合版</option>
            <option value="ryoho">両方</option>
            <option value="others">その他</option>
            </select>
        </div>

        <div class="btn-area">
            <input type="reset" value="リセット！">
            <input type="submit" value="送信！">
        </div>
          
      </form>
    <hr>
    <p class="text-muted text-center">Copyright (C)2021 Shouta.</p>
</body>
</html>