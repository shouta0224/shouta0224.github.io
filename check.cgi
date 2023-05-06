#!/usr/local/bin/perl

#┌─────────────────────────────────
#│ LightBoard : check.cgi - 2021/12/18
#│ copyright (c) kentweb, 1997-2021
#│ https://www.kent-web.com/
#└─────────────────────────────────

# モジュール宣言
use strict;
use CGI::Carp qw(fatalsToBrowser);

# 外部ファイル取り込み
require './init.cgi';
my %cf = set_init();

print <<EOM;
Content-type: text/html; charset=utf-8

<!doctype html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>Check Mode</title>
</head>
<body>
<b>Check Mode: [ $cf{version} ]</b>
<ul>
EOM

# ディレクトリ
for ( $cf{datadir}, "$cf{datadir}/ses", "$cf{datadir}/pwd", "$cf{datadir}/past", "$cf{datadir}/log" ) {
	if (-d $_) {
		print "<li>$_ ディレクトリパス : OK\n";
		
		if (-r $_ && -w $_ && -x $_) {
			print "<li>$_ ディレクトリパーミッション : OK\n";
		} else {
			print "<li>$_ ディレクトリパーミッション : NG\n";
		}
	} else {
		print "<li>$_ ディレクトリパス : NG\n";
	}
}

# ファイルチェック
for (qw(log.cgi conf.cgi pass.dat pastno.dat ses.cgi)) {
	if (-f "$cf{datadir}/$_") {
		print "<li>$cf{datadir}/$_ ファイルパス : OK\n";
		
		if (-r "$cf{datadir}/$_" && -w "$cf{datadir}/$_") {
			print "<li>$_ ファイルパーミッション : OK\n";
		} else {
			print "<li>$_ ファイルパーミッション : NG\n";
		}
	} else {
		print "<li>$_ ファイルパス : NG\n";
	}
}

# テンプレート
foreach (qw(bbs error find conf mesg note past enter del)) {
	if (-f "$cf{tmpldir}/$_.html") {
		print "<li>テンプレート( $_.html ) : OK\n";
	} else {
		print "<li>テンプレート( $_.html ) : NG\n";
	}
}

# Image-Magick動作確認
eval { require Image::Magick; };
if ($@) {
	print "<li>Image-Magick動作: NG\n";
} else {
	print "<li>Image-Magick動作: OK\n";
}

print <<EOM;
</ul>
</body>
</html>
EOM
exit;

