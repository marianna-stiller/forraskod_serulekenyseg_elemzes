<?php
$user_name = mysqli_real_escape_string($con, $_POST["user_name"]);
$password = mysqli_real_escape_string($con, $_POST["password"]);
mysqli_close($con);
?>