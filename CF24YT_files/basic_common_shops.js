// 썸네일 이미지 엑박일경우 기본값 설정
EC$(window).on('load', function() {

    EC$(".thumbnail img, img.thumbImage, img.bigImage").each(function($i,$item){
        var $img = new Image();
        $img.onerror = function () {
            $item.src="//img.echosting.cafe24.com/thumb/img_product_big.gif";
        }
        $img.src = this.src;
    });

});

EC$(function(){
    // 토글
    EC$('div.eToggle .title').off('click').on('click', function() {
        var toggle = EC$(this).parent('.eToggle');
        if(toggle.hasClass('disable') == false){
            EC$(this).parent('.eToggle').toggleClass('selected')
        }

        if(toggle.hasClass('eTermChk')){
            var value = EC$(this).parent('.eToggle').hasClass('selected');
            var layerEl = EC$('#layerJoin .layerContent');
            if(layerEl && value){                
                layerEl.scrollTop(layerEl[0].scrollHeight);                
            }
        }
    });

    EC$('div.eToggle .title .allAgree').on('click', function(e) { 
            e.stopPropagation(); //이용약관 전체동의 클릭시 이벤트 전파 중지
    });

    EC$('dl.eToggle dt').on('click', function() {
        EC$(this).toggleClass('selected');
        EC$(this).next('dd').toggleClass('selected');
    });

    //장바구니 페이지 수량폼 Type 변경
    EC$('[id^="quantity"]').each(function() {
        EC$(this).get(0).type = 'tel';
    });

    // 모바일에서 공급사 테이블 th 강제조절
    EC$('.xans-mall-supplyinfo, .supplyInfo').find('table > colgroup').find('col').eq(0).width(98);
    EC$('.xans-mall-supplyinfo, .supplyInfo').find('th, td').css({padding:'13px 10px 12px'});

    /**
     *  메인카테고리 toggle
     */
    EC$('.xans-product-listmain h2').on('click', function() {
        var bClosed = !!EC$(this).data('is_closed');
        var sUrl;
        if (bClosed) {
            sUrl = "//img.echosting.cafe24.com/skin/mobile_ko_KR/layout/bg_title_close.gif";
        } else {
            sUrl = "//img.echosting.cafe24.com/skin/mobile_ko_KR/layout/bg_title_open.gif";
        }
        EC$(this).css('background-image', 'url("'+ sUrl +'")');
        EC$(this).siblings().toggle();
        EC$(this).parent().find('div.ec-base-paginate').toggle();
        EC$(this).parent().next('div.xans-product-listmore').toggle();
        EC$(this).data('is_closed', !bClosed);
    });

    /* base header 검색 레이어 */
    EC$('#layout .header').find('.search .btnSearch').on('click', function(){
        var $baseHeader = EC$('#layout .header');
        $baseHeader.addClass('open');
        EC$('#dimmedSlider').one('click', function(){
            $baseHeader.removeClass('open');
        });
    });

    /**
     *  상단탑버튼
     */
    var globalTopBtnScrollFunc = function() {
        // 탑버튼 관련변수
        var $btnTop = EC$('#btnTop');

        EC$(window).scroll(function() {
            try {
                var iCurScrollPos = EC$(this).scrollTop();

                if (iCurScrollPos > (EC$(this).height() / 2)) {
                    $btnTop.fadeIn('fast');
                } else {
                    $btnTop.fadeOut('fast');
                }
            } catch(e) { }
        });
    };

    /**
     *  구매버튼
     */
    var globalBuyBtnScrollFunc = function() {
        // 구매버튼 관련변수
        var sFixId = EC$('#orderFixItem').length > 0  ? 'orderFixItem' : 'fixedActionButton',
            $area = EC$('#orderFixArea'),
            $item = EC$('#' + sFixId + '').not($area);

        EC$(window).on('scroll', function() {
            try {
                // 구매버튼 관련변수
                var iCurrentHeightPos = EC$(this).scrollTop() + EC$(this).height(),
                    iButtonHeightPos = $item.offset().top;

                if (iCurrentHeightPos > iButtonHeightPos || iButtonHeightPos < EC$(this).scrollTop() + $item.height()) {
                    if (iButtonHeightPos < EC$(this).scrollTop() - $item.height()) {
                        $area.fadeIn('fast');
                    } else {
                        $area.hide();
                    }
                } else {
                    $area.fadeIn('fast');
                }
            } catch(e) { }
        });
    };

    globalTopBtnScrollFunc();
    globalBuyBtnScrollFunc();
});

// 공통레이어팝업 오픈
var globalLayerOpenFunc = function(_this) {
    this.id = EC$(_this).data('id');
    this.param = EC$(_this).data('param');
    this.basketType = EC$('#basket_type').val();
    this.url = EC$(_this).data('url');
    this.layerId = 'ec_temp_mobile_layer';
    this.layerIframeId = 'ec_temp_mobile_iframe_layer';

    var _this = this;

    function paramSetUrl() {
        if (this.param) {
            // if isset param
        } else {
            this.url = this.basketType ?  this.url + '?basket_type=' + this.basketType : this.url;
        }
    };

    if (this.url) {
        window.ecScrollTop = EC$(window).scrollTop();
        $.ajax({
            url : this.url,
            success : function (data) {
                if (data.indexOf('404 페이지 없음') == -1) {
                    // 있다면 삭제
                    try { EC$(_this).remove(); } catch ( e ) { }

                    var $layer = EC$('<div>', {
                        html: EC$("<iframe>", { src: _this.url, id: _this.layerIframeId, scrolling: 'auto', css: { width: '100%', height: '100%', overflowY: 'auto', border: 0 } } ),
                        id: _this.layerId,
                        css : { position: 'absolute', top: 0, left:0, width: '100%', height: EC$(window).height(), 'z-index': 9999 }
                    });

                    EC$('body').append($layer);
                    EC$('html, body').css({'overflowY': 'hidden', height: '100%', width: '100%'});
                    EC$('#' + this.layerId).show();
                }
            }
        });
    }
};

// 공통레이어팝업 닫기
var globalLayerCloseFunc = function() {
    this.layerId = 'ec_temp_mobile_layer';

    if (window.parent === window)
        self.close();
    else {
        parent.EC$('html, body').css({'overflowY': 'auto', height: 'auto', width: '100%'});
        parent.EC$('html, body').scrollTop(parent.window.ecScrollTop);
        parent.EC$('#' + this.layerId).remove();
    }
};

/**
 * document.location.href split
 * return array Param
 */
var getQueryString = function(sKey)
{
    var sQueryString = document.location.search.substring(1);
    var aParam = {};

    if (sQueryString) {
        var aFields = sQueryString.split("&");
        var aField  = [];
        for (var i=0; i<aFields.length; i++) {
            aField = aFields[i].split('=');
            aParam[aField[0]] = aField[1];
        }
    }

    aParam.page = aParam.page ? aParam.page : 1;
    return sKey ? aParam[sKey] : aParam;
};

// PC버전 바로 가기
var isPCver = function() {
    var sUrl = window.location.hostname;
    var aTemp = sUrl.split(".");

    var pattern = /^(mobile[\-]{2}shop[0-9]+)$/;

    if (aTemp[0] == 'm' || aTemp[0] == 'skin-mobile' || aTemp[0] == 'mobile') {
        sUrl = sUrl.replace(aTemp[0]+'.', '');
    } else if (pattern.test(aTemp[0]) === true) {
        var aExplode = aTemp[0].split('--');
        aTemp[0] = aExplode[1];
        sUrl = aTemp.join('.');
    }
    window.location.href = '//'+sUrl+'/?is_pcver=T';
};

/* 도움말 */
EC$('body').on('click', '.ec-base-tooltip-area .eTip', function(e){
    var findArea = EC$(EC$(this).parents('.ec-base-tooltip-area'));
    var findTarget = EC$(EC$(this).siblings('.ec-base-tooltip'));
    var findTooltip = EC$('.ec-base-tooltip');
    EC$('.ec-base-tooltip-area').removeClass('show');
    EC$(this).parents('.ec-base-tooltip-area').first().addClass('show');
    findTooltip.hide();
    findTarget.show();
    e.preventDefault();
});

EC$('body').on('click', '.ec-base-tooltip-area .eClose', function(e){
    var findTarget = EC$(this).parents('.ec-base-tooltip').first();
    EC$('.ec-base-tooltip-area').removeClass('show');
    findTarget.hide();
    e.preventDefault();
});

EC$('.ec-base-tooltip-area').find('input').on('focusout', function() {
    var findTarget = EC$(this).parents('.ec-base-tooltip-area').find('.ec-base-tooltip');
    EC$('.ec-base-tooltip-area').removeClass('show');
    findTarget.hide();
});

/**
 * 팝업창에 리사이즈 관련
 */

function setResizePopup() {

    if(!EC$('#popup').length) return;

    var iWrapWidth    = EC$('#popup').width();
    var iWrapHeight   = EC$('#popup').height();

    var iWindowWidth  = EC$(window).width();
    var iWindowHeight = EC$(window).height();

    window.resizeBy(iWrapWidth - iWindowWidth, iWrapHeight - iWindowHeight);
}
setResizePopup();

// 팝업 페이지 로드가 완료된 후에 리사이징 함수를 다시 호출
EC$( window ).on('load', function() {
    setResizePopup();
});

/**
 * eLayerModal
 **/
var bodyEl = document.querySelector('body'); 
var links = document.querySelectorAll('.eLayerModal');
var targetDiv = null;

links.forEach(function(link) {
  link.addEventListener('click', function(event) {
    var href = this.getAttribute('href');
    var id = href.substring(1);
    
    targetDiv = document.getElementById(id);    
    targetDiv.classList.add('show');
    bodyEl.classList.add('overflowHidden');

    event.preventDefault();
  });
});

var closeBtn = document.querySelectorAll('.layerFooter .eClose');

closeBtn.forEach(function(closeEl) {
    closeEl.addEventListener('click', function() {
        if(targetDiv){
            targetDiv.classList.remove('show');
            bodyEl.classList.remove('overflowHidden');
        }
    });
});

