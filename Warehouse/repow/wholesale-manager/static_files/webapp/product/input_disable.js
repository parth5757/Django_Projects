$(function() {
    $inp = $("#id_weight");
    $cb = $("#id_is_apply_weight");
    $inp1 = $("#id_ml_quantity");
    $cb1 = $("#id_is_apply_ml_quantity");

    $inp2 = $("#id_box_piece"); 
    $cb2 = $("#id_box");
    $inp3 = $("#id_case_piece");  
    $cb3 = $("#id_case");


    $inp.prop('disabled', true);
    $inp1.prop('disabled', true);
    $inp2.prop('disabled', true);
    $inp3.prop('disabled', true);

    if ($cb.is(':checked')) {
      $inp.prop('disabled', false);
    };
    $cb.on('change', function() {
      if ($cb.is(':checked')) {
        $inp.prop('disabled', false);
      } else {
        $inp.val(0.0)
        $inp.prop('disabled', true);

      }
    });
    if ($cb1.is(':checked')) {
      $inp1.prop('disabled', false);
    };
    $cb1.on('change', function() {
      if ($cb1.is(':checked')) {
        $inp1.prop('disabled', false);
      } else {
        $inp1.val(0)
        $inp1.prop('disabled', true);
      }
    });
    if ($cb2.is(':checked')) {
      $inp2.prop('disabled', false);
    }
    $cb2.on('change', function() {
      if ($cb2.is(':checked')) {
        $inp2.prop('disabled', false);
      } else {
        $inp2.prop('disabled', true);
        $inp2.val(0)

      }
    });
    if ($cb3.is(':checked')) {
      $inp3.prop('disabled', false);
    }
    $cb3.on('change', function() {
      if ($cb3.is(':checked')) {
        $inp3.prop('disabled', false);
      } else {
        $inp3.prop('disabled', true);
        $inp3.val(0)

      }
    });
  
  });