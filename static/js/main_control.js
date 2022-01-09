function get_time() {
    $.ajax({
        url: "/time",
        timeout: 10000,
        success:function(data) {
            $("#time").text("Last update: " + data)
        },
        error:function() {

        }
    });        
}

function get_c1_data() {
    $.ajax({
        url: "/c1",
        timeout: 10000,
        success:function(data) {
            $(".num h1").eq(0).html(data.confirm);
            $(".num h1").eq(1).html(data.suspect);
            $(".num h1").eq(2).html(data.heal);
            $(".num h1").eq(3).html(data.dead);
        },
        error:function() {

        }
    })
}

function get_c2_data() {
    $.ajax({
        url: "/c2",
        timeout: 10000,
        success:function(data) {
            ec_center_option.series[0].data = data.data
            ec_center.setOption(ec_center_option)
        },
        error:function() {

        }
    })
}

function get_l1_data() {
    $.ajax({
        url:"/l1",
        success: function(data) {
			ec_left1_Option.xAxis[0].data=data.day
            ec_left1_Option.series[0].data=data.confirm
            ec_left1_Option.series[1].data=data.heal
            ec_left1_Option.series[2].data=data.dead
            ec_left1.setOption(ec_left1_Option)
		},
		error: function() {

		}
    })
}

function get_l2_data() {
    $.ajax({
        url:"/l2",
        success: function(data) {
			ec_left2_Option.xAxis[0].data=data.day
            ec_left2_Option.series[0].data=data.confirm_add
            ec_left2_Option.series[1].data=data.suspect_add
            ec_left2.setOption(ec_left2_Option)
		},
		error: function() {

		}
    })
}

get_time()
get_c1_data()
get_c2_data()
get_l1_data()
get_l2_data()

setInterval(get_time,1000*10)
setInterval(get_c1_data,1000*10)
setInterval(get_c2_data,10000*10)
setInterval(get_l1_data,10000*10)
setInterval(get_l2_data,10000*10)
