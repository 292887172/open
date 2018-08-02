
		$(document).ready(function(){

			function myfunction(li,li_a,menu_tab){
				li.click(function(){
				var index=$(this).index();
				menu_tab.eq(index).addClass("active").siblings().removeClass("active");
				li_a.removeClass("selected");
				li_a.eq(index).addClass("selected").siblings().removeClass("selected");
				
			});
			}

			myfunction($(".container .menu .ulmenu1 li"),$(".container .ulmenu1 li a"),$(".container .content .menu1 .tab"));

		});



