document.addEventListener("DOMContentLoaded", function () {

    let post_dates = document.getElementsByClassName("post-date");

    let now = new Date();

    for (let single_date of post_dates) {
        let html = single_date.innerHTML;

        // gathering position pointers
        let month_pos = html.indexOf('.') + 2;
        let year_pos = html.indexOf(',') + 2;
        let hour_pos = html.indexOf(':');

        // gathering date details for month, day, etc.
        let month = html.substring(0, 3);
        let day = parseInt(html.substring(month_pos, month_pos + 2));
        let year = html.substring(year_pos, year_pos + 4);
        let ampm = html.substring(hour_pos + 4, hour_pos + 5);

        // am/pm conversion
        let pre_hour = html.substring(hour_pos - 2, hour_pos);
        let hour;
        let min = html.substring(hour_pos + 1, hour_pos + 3);
        if (ampm == "p") {
            if (pre_hour == 12) {
                hour = pre_hour;
            } else {
                hour = pre_hour + 12;
            }
        } else {
            if (pre_hour == 12) {
                hour = 0;
            } else {
                hour = pre_hour;
            }
        }

        // converted date string for difference calculations
        let date_string = new Date(month + " " + day + ", " + year + " " + hour + ":" + min);

        // difference calculations
        let diff = now - date_string;
        let diff_display;
        let diff_mins = Math.floor((diff / 1000) / 60);
        let diff_hours = Math.floor(((diff / 1000) / 60) / 60);
        let diff_days = Math.floor((((diff / 1000) / 60) / 60) / 24);
        if (diff_days == 0) {
            if (diff_hours == 0) {
                diff_display = diff_mins + "m";
            } else {
                diff_display = diff_hours + "h";
            }
        } else {
            diff_display = diff_days + "d";
        }

        // display the result
        single_date.innerHTML = diff_display + " ago @ " + html;

    }
});