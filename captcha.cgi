#!/usr/local/bin/perl

#┌─────────────────────────────
#│ 画像認証作成（セッション式） v4.1
#│ captcha.cgi - 2021/03/10
#│ copyright (c) kentweb
#│ https://www.kent-web.com/
#└─────────────────────────────

# モジュール宣言
use strict;

# 外部ファイル取り込み
require './init.cgi';
my %cf = set_init();

# パラメータ受け取り
my $buf = $ENV{QUERY_STRING};
$buf =~ s/\W//g;
err_img() if (!$buf);

# 数字取得
my $digit = pickout_dig($buf);

# 認証画像作成
if ($cf{use_captcha} == 2) {
	require $cf{captsec_pl};
	load_capsec($digit,"$cf{bin_dir}/$cf{font_ttl}");
} else {
	require $cf{pngren_pl};
	load_pngren($digit,"$cf{bin_dir}/$cf{si_png}");
}

#-----------------------------------------------------------
#  認証画像作成 [ライブラリ版]
#-----------------------------------------------------------
sub load_pngren {
	my ($plain,$sipng) = @_;
	
	# 数字
	my @img = split(//,$plain);
	
	# PNG表示
	pngren::PngRen($sipng,\@img);
	exit;
}

#-----------------------------------------------------------
#  数字抽出
#-----------------------------------------------------------
sub pickout_dig {
	my $ses = shift;
	
	my $dig;
	open(IN,"$cf{datadir}/conf.cgi") or err_img();
	while(<IN>) {
		chomp;
		my ($time,$rand,$fig) = split(/\t/);
		
		if ($ses eq $rand) {
			$dig = $fig;
			last;
		}
	}
	close(IN);
	
	# 結果を返す
	return $dig ne '' ? $dig : err_img();
}

#-----------------------------------------------------------
#  エラー処理
#-----------------------------------------------------------
sub err_img {
	# エラー画像
	my @err = qw(
		47 49 46 38 39 61 2d 00 0f 00 80 00 00 00 00 00 ff ff ff 2c
		00 00 00 00 2d 00 0f 00 00 02 49 8c 8f a9 cb ed 0f a3 9c 34
		81 7b 03 ce 7a 23 7c 6c 00 c4 19 5c 76 8e dd ca 96 8c 9b b6
		63 89 aa ee 22 ca 3a 3d db 6a 03 f3 74 40 ac 55 ee 11 dc f9
		42 bd 22 f0 a7 34 2d 63 4e 9c 87 c7 93 fe b2 95 ae f7 0b 0e
		8b c7 de 02	00 3b
	);
	
	print "Content-type: image/gif\n\n";
	foreach (@err) {
		print pack('C*',hex($_));
	}
	exit;
}

