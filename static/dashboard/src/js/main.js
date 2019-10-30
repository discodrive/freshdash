'use strict';
jQuery(document).ready(function($) {

    $('.c-event-toggle__grid').click(function(){
        $('.c-clients-list').removeClass('state--client-list').addClass('state--client-grid');
        $('.client-list').addClass('columns is-multiline');
        $('.c-single-client').addClass('column is-one-third')
        $('.headings').css('display', 'none');
    });

    $('.c-event-toggle__list').click(function(){
        $('.c-clients-list').removeClass('state--client-grid').addClass('state--client-list');
        $('.client-list').removeClass('columns');
        $('.c-single-client').removeClass('column is-one-third')
        $('.headings').css('display', 'block');
    });

});