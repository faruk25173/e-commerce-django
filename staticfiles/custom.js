$(document).ready(function(){
	$("#loadMore").on('click',function(){
		var _currentProducts=$(".product-box").length;
		var _limit=$(this).attr('data-limit');
		var _total=$(this).attr('data-total');
		// Start Ajax
		$.ajax({
			url:'/load-more-data',
			data:{
				limit:_limit,
				offset:_currentProducts
			},
			dataType:'json',
			beforeSend:function(){
				$("#loadMore").attr('disabled',true);
				$(".load-more-icon").addClass('fa-spin');
			},
			success:function(res){
				$("#filteredProducts").append(res.data);
				$("#loadMore").attr('disabled',false);
				$(".load-more-icon").removeClass('fa-spin');

				var _totalShowing=$(".product-box").length;
				if(_totalShowing==_total){
					$("#loadMore").remove();
				}
			}
		});
		// End
	});

	// Product Variation

	    $(".choose-size").hide();
	    $(".product-images").hide();


	    $(".choose-color").on('click',function(){
		var _color=$(this).attr('data-color');
		var _colors=$(this).attr('data-colors');
		var _img=$(this).attr('data-img');

		$(".choose-size").hide();
		$(".product-images").hide();
		//$(".product-imagem").hide();


		$(".color"+_color).show();
		$(".img"+_img).show();
        $(".product-color").text(_colors);

		$(".color"+_color).first().addClass('active');
		$(".img"+_img).first().addClass('active');

        });


	    $(".choose-size").on('click',function(){
		$(".choose-size").removeClass('active');
		$(this).addClass('active');

		var _price=$(this).attr('data-price');
		var _quantity=$(this).attr('data-quantity');
		//var _color=$(this).attr('data-color');
		var _size=$(this).attr('data-size');
		var _id=$(this).attr('data-id');

		var _image=$(this).attr('data-image');




		$(".product-price").text(_price);
		$(".product-quantity").text(_quantity);
		//$(".product-color").text(_color);
		$(".product-size").text(_size);
		$(".product-id").val(_id);
		$(".product-image").val(_image);
	    });

		var _color=$(".choose-color").first().attr('data-color');
		var _price=$(".choose-size").first().attr('data-price');

		$(".color"+_color).show();
		$(".color"+_color).first().addClass('active');
		$(".product-price").text(_price);

		var _img=$(".choose-color").first().attr('data-img');
		$(".img"+_img).show();
		$(".img"+_img).first().addClass('active');


//		var _imgm=$(".product-imagem").first().attr('data-ids');
//		$(".imgm"+_imgm).show();
//		$(".imgm"+_imgm).first().addClass('active');




        $(".product-imagem").hide();
		$(".product-imgs").on('click',function(){
		var _imgs=$(this).attr('data-ids');
        $(".product-imagem").hide();
        $(".imgm"+_imgs).show();
        $(".imgm"+_imgs).first().addClass('active');

         });
         var _imgs=$(".product-imgs").first().attr('data-ids');
         $(".imgm"+_imgs).show();
         $(".imgm"+_imgs).first().addClass('active');


	// End

	 $(document).on('click',".add-to-cart",function(){
        var _vm=$(this);
        var _index=_vm.attr('data-index');
        var _qty=$(".product-qty-"+_index).val();
        var _productTitle=$(".product-title-"+_index).val();
        var _productId=$(".product-id-"+_index).val();
        var _productImage=$(".product-image-"+_index).val();
        var _productPrice=$(".product-price-"+_index).text();
        var _productColor=$(".product-color-"+_index).text();
        var _productSize=$(".product-size-"+_index).text();

        var _quantity=$(".product-quantity-"+_index).text();


            if ( _quantity<_qty)
            {
             alert("Please check quantity in stock")
            }
            else {
                // Ajax
                $.ajax({
                    url:'/add-to-cart',
                    data:{
                        'id':_productId,
                        'image':_productImage,
                        'title':_productTitle,
                        'qty':_qty,
                        'price':_productPrice,
                        'color':_productColor,
                        'size':_productSize,
                    },
                    dataType:'json',
                    beforeSend:function(res){
                        _vm.attr('disabled',true);
                    },
                    success:function(res){
                        $(".cart-list").text(res.totalitems);
                        _vm.attr('disabled',false);

                   if(res!==null){
                         alert("Product Added")
                         }
                         else{
                          alert("This Product Already Added")
                         }
                    }

                 });

            }


	});
	// End

	// Delete item from cart
	$(document).on('click','.delete-item',function(){
		var _pId=$(this).attr('data-item');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/delete-from-cart',
			data:{
				'id':_pId,
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);
			}
		});
		// End
	});

	// Update item from cart
	$(document).on('click','.update-item',function(){
		var _pId=$(this).attr('data-item');
		var _pQty=$(".product-qty-"+_pId).val();
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/update-cart',
			data:{
				'id':_pId,
				'qty':_pQty
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				// $(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);
			}
		});
		// End
	});

	// Add wishlist
	$(document).on('click',".add-wishlist",function(){
		var _pid=$(this).attr('data-product');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:"/add-wishlist",
			data:{
				product:_pid
			},
			dataType:'json',
			success:function(res){
				if(res.bool==true){
					_vm.addClass('disabled').removeClass('add-wishlist');

					 if(res!==null){
                         alert("Product Added to WishList")
                         }
                         else{
                          alert("This Product Already Added to WishList")
                         }
				}
			}
		});
		// EndAjax
	});
	// End

	$(document).on('click','.wish-remove',function(){
		var _pId=$(this).attr('data-item');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/remove-item',
			data:{
				'id':_pId,
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
			$("#wishList").text(res.wlist);
				_vm.attr('disabled',false);
				$("#wishList").html(res.data);

			}
		});
		// End
	});

	// Activate selected address
	$(document).on('click','.activate-address',function(){
		var _aId=$(this).attr('data-address');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/activate-address',
			data:{
				'id':_aId,
			},
			dataType:'json',
			success:function(res){
				if(res.bool==true){
					$(".address").removeClass('shadow border-secondary');
					$(".address"+_aId).addClass('shadow border-secondary');

					$(".check").hide();
					$(".actbtn").show();

					$(".check"+_aId).show();
					$(".btn"+_aId).hide();
				}
			}
		});
		// End
	});

});
// End Document.Ready

// Product Review Save
$("#addForm").submit(function(e){
	$.ajax({
		data:$(this).serialize(),
		method:$(this).attr('method'),
		url:$(this).attr('action'),
		dataType:'json',
		success:function(res){
			if(res.bool==true){
				$(".ajaxRes").html('Data has been added.');
				$("#reset").trigger('click');
				// Hide Button
				$(".reviewBtn").hide();
				// End

				// create data for review
				var _html='<blockquote class="blockquote text-right">';
				_html+='<small>'+res.data.review_text+'</small>';
				_html+='<footer class="blockquote-footer">'+res.data.user;
				_html+='<cite title="Source Title">';
				for(var i=1; i<=res.data.review_rating; i++){
					_html+='<i class="fa fa-star text-warning"></i>';
				}
				_html+='</cite>';
				_html+='</footer>';
				_html+='</blockquote>';
				_html+='</hr>';

				$(".no-data").hide();

				// Prepend Data
				$(".review-list").prepend(_html);

				// Hide Modal
				$("#productReview").modal('hide');

				// AVg Rating
				$(".avg-rating").text(res.avg_reviews.avg_rating.toFixed(1))
			}
		}
	});
	e.preventDefault();
});
// End