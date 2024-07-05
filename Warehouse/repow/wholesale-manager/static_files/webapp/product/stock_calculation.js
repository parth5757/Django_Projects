function get_total(){
    piece_total = parseInt($("#id_piece_total").val())
    if($("#id_box_total").val()){
        box_total = parseInt($("#id_box_total").val())
    }
    else{
        box_total = 0
    }

    if($("#id_case_total").val()){
        case_total = parseInt($("#id_case_total").val())
    }
    else{
        case_total = 0
    }
    sum = piece_total + box_total + case_total
    return sum
}
$(document).on('change keyup', '#id_piece', function () {
    quntity = $('#id_piece').val()
    id_stock=$("#id_stock")
    piece_total = $('#id_piece_total')
    piece_total.val(quntity)
    id_stock.val(get_total())

});
$(document).on('change keyup', '#id_box', function () {
    quntity = $('#id_box').val()
    id_stock=$("#id_stock")
    pieceperbox=$('#id_box_piece').val()
    piece_total = $('#id_box_total')
    piece_total.val(parseInt(quntity)*parseInt((pieceperbox)))
    id_stock.val(get_total())


});
$(document).on('change keyup', '#id_case', function () {
    quntity = $('#id_case').val()
    piecepercase=$('#id_case_piece').val()
    id_stock=$("#id_stock")
    piece_total = $('#id_case_total')
    piece_total.val(parseInt(quntity)*parseInt((piecepercase)))
    id_stock.val(get_total())
});