<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    $apiKey = $_POST["apiKey"];

    // Afiseaza pentru debbuging
    echo "Username: " . $username . "<br>";
    echo "API Key: " . $apiKey . "<br>";

    // paseaza username si apikey la shell script
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
