<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    $apiKey = $_POST["apiKey"];

    // Displaying username and apiKey for debugging
    echo "Username: " . $username . "<br>";
    echo "API Key: " . $apiKey . "<br>";

    // Execute the shell script passing username and apiKey as arguments
    $output = shell_exec("/var/www/html/add_user.sh '$username' '$apiKey' 2>&1");
   echo "!!!";
   echo "$output";
   echo "!!!";
    if ($output !== null) {
        echo "User added successfully.";
    } else {
        echo "Failed to add user. Error: $output";
    }
}
?>
