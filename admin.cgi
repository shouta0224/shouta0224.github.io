#!/usr/local/bin/perl

#┌─────────────────────────────────
#│ LightBoard : admin.cgi - 2021/12/18
#│ copyright (c) kentweb, 1997-2021
#│ https://www.kent-web.com/
#└─────────────────────────────────

# モジュール宣言
use strict;
use CGI::Carp qw(fatalsToBrowser);
use vars qw(%in %cf);
use lib "./lib";
use CGI::Session;
use Digest::SHA::PurePerl qw(sha256_base64);

# 設定ファイル認識
require "./init.cgi";
%cf = set_init();

# データ受理
%in = parse_form();

# 認証
require "./lib/login.pl";
auth_login();

# 条件分岐
if ($in{data_men}) { data_men(); }
if ($in{data_app}) { data_app(); }
if ($in{pass_mgr}) { pass_mgr(); }

# 管理モード
menu_html();

#-----------------------------------------------------------
#  メニュー画面
#-----------------------------------------------------------
sub menu_html {
	header("メニューTOP");
	print <<EOM;
<div id="body">
<div align="center">
<p>選択ボタンを押してください。</p>
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="sid" value="$in{sid}">
<table class="form-tbl">
<tr>
	<th></th>
	<th width="300">処理メニュー</th>
</tr><tr>
	<td class="ta-c"><input type="submit" name="data_men" value="選択"></td>
	<td>記事管理</td>
EOM

	if ($cf{approve} == 1) {
		print qq|</tr><tr>\n|;
		print qq|<td class="ta-c"><input type="submit" name="data_app" value="選択"></td>\n|;
		print qq|<td>投稿記事の承認/反映</td>\n|;
	}
	
	print <<EOM;
</tr><tr>
	<td class="ta-c"><input type="submit" name="pass_mgr" value="選択"></td>
	<td>パスワード管理</td>
</tr><tr>
	<td class="ta-c"><input type="submit" name="logoff" value="選択"></td>
	<td>ログアウト</td>
</tr>
</table>
</form>
</div>
</div>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  記事メンテナンス
#-----------------------------------------------------------
sub data_men {
	# 削除処理
	if ($in{job} eq "dele" && $in{no}) {
		
		# 削除情報
		my %del;
		foreach ( split(/\0/,$in{no}) ) {
			$del{$_}++;
		}
		
		# 削除情報をマッチング
		my @data;
		open(DAT,"+< $cf{datadir}/log.cgi") or cgi_err("open err: log.cgi");
		eval "flock(DAT,2);";
		while (<DAT>) {
			my ($no) = (split(/<>/))[0];
			
			if (!defined($del{$no})) {
				push(@data,$_);
			}
		}
		
		# 更新
		seek(DAT, 0, 0);
		print DAT @data;
		truncate(DAT, tell(DAT));
		close(DAT);
	
	# 修正画面
	} elsif ($in{job} eq "edit" && $in{no}) {
		
		my @data;
		open(IN,"$cf{datadir}/log.cgi") or cgi_err("open err: log.cgi");
		while (<IN>) {
			my ($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd,$tim) = split(/<>/);
			
			if ($in{no} == $no) {
				@data = ($no,$dat,$nam,$eml,$sub,$com,$url);
				last;
			}
		}
		close(IN);
		
		# 修正フォームへ
		edit_form(@data);
	
	# 修正実行
	} elsif ($in{job} eq "edit2") {
		
		# 未入力の場合
		if ($in{url} eq "http://") { $in{url} = ""; }
		$in{sub} ||= "無題";
		
		# 読み出し
		my @data;
		open(DAT,"+< $cf{datadir}/log.cgi") or cgi_err("open err: log.cgi");
		eval "flock(DAT,2);";
		while (<DAT>) {
			my ($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd,$tim) = split(/<>/);
			
			if ($in{no} == $no) {
				$_ = "$no<>$dat<>$in{name}<>$in{email}<>$in{sub}<>$in{comment}<>$in{url}<>$hos<>$pwd<>$tim<>\n";
			}
			push(@data,$_);
		}
		
		# 更新
		seek(DAT, 0, 0);
		print DAT @data;
		truncate(DAT, tell(DAT));
		close(DAT);
		
		# 完了メッセージ
		message("記事を修正しました");
	}
	
	# 記事メンテナンス画面を表示
	header("記事メンテナンス");
	back_btn();
	print <<EOM;
<div id="body">
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="data_men" value="1">
<input type="hidden" name="sid" value="$in{sid}">
処理：
<select name="job">
<option value="edit">修正
<option value="dele">削除
</select>
<input type="submit" value="送信する">
EOM

	# 記事を展開
	open(IN,"$cf{datadir}/log.cgi") or cgi_err("open err: log.cgi");
	while (<IN>) {
		my ($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd,$tim) = split(/<>/);
		$nam = qq|<a href="mailto:$eml">$nam</a>| if ($eml);
		
		print qq|<div class="art"><input type="checkbox" name="no" value="$no">\n|;
		print qq|[$no] <strong>$sub</strong> 投稿者：$nam 日時：$dat [ <span>$hos</span> ]</div>\n|;
		print qq|<div class="com">| . cut_str($com,50) . qq|</div>\n|;
	}
	close(IN);
	
	print <<EOM;
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  修正フォーム
#-----------------------------------------------------------
sub edit_form {
	my ($no,$dat,$nam,$eml,$sub,$com,$url) = @_;
	
	$com =~ s|<br( /)?>|\n|g;
	$url ||= "http://";
	
	header("記事メンテナンス &gt; 修正フォーム");
	back_btn('mente_log');
	print <<EOM;
<div id="body">
<ul>
<li>変更する部分のみ修正して送信ボタンを押してください。
</ul>
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="data_men" value="1">
<input type="hidden" name="job" value="edit2">
<input type="hidden" name="no" value="$no">
<input type="hidden" name="sid" value="$in{sid}">
<table class="form-tbl">
<tr>
  <th>おなまえ</th>
  <td><input type="text" name="name" size="28" value="$nam"></td>
</tr><tr>
  <th>e-mail</th>
  <td><input type="text" name="email" size="28" value="$eml"></td>
</tr><tr>
  <th>タイトル</th>
  <td><input type="text" name="sub" size="36" value="$sub"></td>
</tr><tr>
  <th>参照先</th>
  <td><input type="text" name="url" size="50" value="$url"></td>
</tr><tr>
  <th>コメント</th>
  <td>
    <textarea name="comment" cols="60" rows="7">$com</textarea><br>
	<input type="submit" value="送信する"><input type="reset" value="リセット">
  </th>
</tr>
</table>
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  投稿記事の承認・反映
#-----------------------------------------------------------
sub data_app {
	# 承認
	if ($in{job} eq 'aprv' && $in{no}) {
		
		my @data;
		foreach ( split(/\0/, $in{no}) ) {
			open(IN,"$cf{datadir}/log/$_.cgi");
			my $log = <IN>;
			close(IN);
			
			push(@data,$log);
		}
		my $data = @data;
		
		open(DAT,"+< $cf{datadir}/log.cgi") or cgi_err("open err: log.cgi");
		eval "flock(DAT,2);";
		my $top = <DAT>;
		
		my ($num) = (split(/<>/, $top))[0];
		
		# 最大記事数処理
		my $i = 0;
		my (@log,@old);
		seek(DAT, 0, 0);
		while (<DAT>) {
			$i++;
			my ($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$tim) = split(/<>/);
			
			if ($i <= $cf{maxlog} - $data) {
				push(@log,$_);
			} else {
				push(@old,$_);
			}
		}
		
		# 新記事
		foreach (@data) {
			$num++;
			unshift(@log,"$num<>$_\n");
		}
		
		# 更新
		seek(DAT,0,0);
		print DAT @log;
		truncate(DAT,tell(DAT));
		close(DAT);
		
		# 過去ログ更新
		if ($cf{pastkey} && @old > 0) { make_pastlog(@old); }
		
		# 一時ファイル削除
		foreach ( split(/\0/,$in{no}) ) {
			unlink("$cf{datadir}/log/$_.cgi");
		}
	
	# 削除
	} elsif ($in{job} eq 'dele' && $in{no}) {
		foreach ( split(/\0/,$in{no}) ) {
			unlink("$cf{datadir}/log/$_.cgi");
		}
	}
	
	# 記事メンテナンス画面を表示
	header("投稿記事の承認/反映");
	back_btn();
	print <<EOM;
<div id="body">
<p class="ttl">■ 投稿記事の承認/反映</p>
<ul>
<li>「承認」又は「削除」を選択して送信ボタンを押してください。やり直しはできないので慎重に！
</ul>
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="data_app" value="1">
<input type="hidden" name="sid" value="$in{sid}">
処理：
<select name="job">
<option value="aprv">承認
<option value="dele">削除
</select>
<input type="submit" value="送信する">
EOM

	opendir(DIR,"$cf{datadir}/log");
	while( $_ = readdir(DIR) ) {
		next if (!/^(\d+)\.cgi$/);
		
		my $num = $1;
		open(IN,"$cf{datadir}/log/$num.cgi");
		my $log = <IN>;
		close(IN);
		
		my ($date,$nam,$eml,$sub,$com,$url,$hos,$pw,$tim) = split(/<>/,$log);
		print qq|<div class="art"><input type="checkbox" name="no" value="$num">\n|;
		print qq|<strong>$sub</strong> 投稿者：<b>$nam</b> 投稿日：$date [ <span>$hos</span> ]</div>\n|;
		print qq|<div class="com">$com</div>\n|;
	}
	closedir(DIR);
	
	print <<EOM;
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  HTMLヘッダー
#-----------------------------------------------------------
sub header {
	my $ttl = shift;
	
	print <<EOM;
Content-type: text/html; charset=utf-8

<!doctype html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<link href="$cf{cmnurl}/admin.css" rel="stylesheet">
<title>$ttl</title>
</head>
<body>
<div id="head">LIGHT BOARD 管理画面 ::</div>
EOM
}

#-----------------------------------------------------------
#  エラー
#-----------------------------------------------------------
sub cgi_err {
	my $err = shift;
	
	header("ERROR!");
	print <<EOM;
<div id="err">
<p><b>ERROR!</b></p>
<p class="err">$err</p>
<p><input type="button" value="前画面に戻る" onclick="history.back()"></p>
</div>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  完了メッセージ
#-----------------------------------------------------------
sub message {
	my $msg = shift;
	
	header("完了");
	print <<EOM;
<div id="msg">
<p>$msg</p>
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="sid" value="$in{sid}">
<input type="submit" value="管理画面に戻る">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  戻りボタン
#-----------------------------------------------------------
sub back_btn {
	my $mode = shift;
	
	print <<EOM;
<div class="back-btn">
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="sid" value="$in{sid}">
@{[ $mode ? qq|<input type="submit" name="$mode" value="&lt; 前画面">| : "" ]}
<input type="submit" value="▲メニュー">
</form>
</div>
EOM
}

#-----------------------------------------------------------
#  文字カット for UTF-8
#-----------------------------------------------------------
sub cut_str {
	my ($str,$all) = @_;
	$str =~ s|<br( /)?>||g;
	
	my $i = 0;
	my ($ret,$flg);
	while ($str =~ /([\x00-\x7f]|[\xC0-\xDF][\x80-\xBF]|[\xE0-\xEF][\x80-\xBF]{2}|[\xF0-\xF7][\x80-\xBF]{3})/gx) {
		$i++;
		$ret .= $1;
		if ($i >= $all) {
			$flg++;
			last;
		}
	}
	$ret .= '...' if ($flg);
	
	return $ret;
}

