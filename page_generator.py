def get_base(title):
    return """<!DOCTYPE html>
<html lang="en">
<head>
	<title>{}</title>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
<!--===============================================================================================-->	
	<link rel="icon" type="image/png" href="images/icons/favicon.ico"/>
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/bootstrap/css/bootstrap.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="fonts/font-awesome-4.7.0/css/font-awesome.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/animate/animate.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/select2/select2.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/perfect-scrollbar/perfect-scrollbar.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="css/util.css">
	<link rel="stylesheet" type="text/css" href="css/main.css">
<!--===============================================================================================-->
</head>
<body>
	
	<div class="limiter">
		<div class="container-table100">
			<div class="wrap-table100">
				<div class="table100 ver1 m-b-110">
					<table data-vertable="ver1">""".format(
        title
    )


def get_thead(
    data=(
        "Section name",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
    ),
):
    head_columns = ["""<thead> <tr class="row100 head">"""]
    for i in range(1, len(data) + 1):
        head_columns.append(
            """<th class="column100 column{}" data-column="column{}">{}</th>""".format(
                i, i, data[i - 1]
            )
        )
    head_columns.append("</tr></thead><tbody>")
    return "\n".join(head_columns)


def data_start():
    return """<tr class="row100">"""


def data_end():
    return "</tr>"


def get_data(course_name, data):
    head_data = []
    info = ["--" for i in range(8)]
    for n, i in enumerate(data["day"]):
        info[n] = i

    for i in range(1, len(data) + 1):
        if i == 1:
            head_data.append(
                """<td class="column100 column{}" data-column="column{}">{}</td>""".format(
                    i, i, course_name
                )
            )
        else:
            head_data.append(
                """<td class="column100 column{}" data-column="column{}">{}</td>""".format(
                    i, i, data[i - 1]
                )
            )
    return "\n".join(head_data)


def get_end():
    return """<!--===============================================================================================-->	
	<script src="vendor/jquery/jquery-3.2.1.min.js"></script>
<!--===============================================================================================-->
	<script src="vendor/bootstrap/js/popper.js"></script>
	<script src="vendor/bootstrap/js/bootstrap.min.js"></script>
<!--===============================================================================================-->
	<script src="vendor/select2/select2.min.js"></script>
<!--===============================================================================================-->
	<script src="js/main.js"></script>

</body>
</html>"""

