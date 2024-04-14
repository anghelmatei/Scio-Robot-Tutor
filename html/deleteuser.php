<?php
$username = $_POST['username'];
$output = shell_exec("bash deleteuser.sh $username 2>&1");
echo $output;
?>
