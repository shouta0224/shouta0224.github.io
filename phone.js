$(function () {
    if (isMobile.any) {
        $('.mobile-check').text('モバイル端末です');
        $('.device').css('display', 'block');
        if (isMobile.apple.phone) {
            $('.mobile-check02').text('iPhoneです');
        } else if (isMobile.apple.tablet) {
            $('.mobile-check02').text('iPadです');
        } else if (isMobile.apple.device) {
            $('.mobile-check02').text('Appleです');
        } else if (isMobile.android.phone) {
            $('.mobile-check02').text('Android(スマホ)です');
        } else if (isMobile.android.tablet) {
            $('.mobile-check02').text('Android(タブレット)です');
        } else if (isMobile.android.device) {
            $('.mobile-check02').text('Androidです');
        } else {
            $('.mobile-check02').text('');
        }
    } else {
        $('.device').css('display', 'none');
        $('.mobile-check').text('モバイル端末ではありません');
    }
});