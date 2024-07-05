var utils = {


    inlineFormSLMEmailAdd: function(id, mgmt_form_id, callback) {
        $(document).on('click', '#add-email-inline', function() {
            event.preventDefault();
            var template_markup = $(`#${id}-template`).html();
            var count = parseInt($(`#id_${mgmt_form_id}-TOTAL_FORMS`).attr('value'), 10);
            var compiled_template = template_markup.replace(/__prefix__/g, count);
            $(`#${id}-table tbody`).append(compiled_template);
            $(`#id_${mgmt_form_id}-TOTAL_FORMS`).attr('value', count + 1);
            $('.btn-inline-remove').hide();

            if (callback != undefined) {
                callback();
            }

        });
    },


    inlineFormRemove: function(table = null) {
        $(document).on('click', '.inlineform-remove', function() {
            $(this).parent().find('input[type=checkbox]').trigger('click');
            $(this).parent().parent().hide();
        });
    }

}


// this code for checkbox in inline view contact details
        // when user click one check then move two send so when first is disable
    var $checks = $('input[type="checkbox"]');
    $checks.click(function() {
    $checks.not(this).prop("checked", false);
    });
//----END---

    $(document).on('click', 'input[type="checkbox"]', function() {      
        $('input[type="checkbox"]').not(this).prop('checked', false);      
    });
    
    // $('.id_customer-NaN-is_default').on('change', function() {
    //     $('.id_customer-NaN-is_default').not(this).prop('checked', false);  
    // });
