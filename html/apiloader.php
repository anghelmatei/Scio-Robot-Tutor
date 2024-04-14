<?php
// Retrieve username or API key holder from the POST request
$username = $_POST['apiKey'];

// Debugging: Output the username to see what is being passed
echo "Username received: $username\n";

// Retrieve output to search for the key
$output = shell_exec('./displaydb.sh 2>&1');

// Search for the key
if ($output !== null) {
    // Split output into an array of rows
    $rows = explode("\n", $output);

    // Loop through each row to find the username and corresponding API key
    foreach ($rows as $row) {
        // Skip empty rows
        if (empty($row)) {
            continue;
        }

        // Split each row into columns
        $columns = explode("|", $row);

        // Check if the first column (username) matches the provided username
        if (trim($columns[0]) === $username) {
            // If the username matches, retrieve the API key from the second column
            $apiKey = trim($columns[1]);
            echo "ApiKey Found: $apiKey\n";

            // Set the API key using envkeymod.sh
            $envKeyModCommand = "bash envkeymod.sh " . $apiKey;
            $output = shell_exec($envKeyModCommand);

            // Output the output of envkeymod.sh
            echo "envkeymod.sh output: $output\n";

            // Check if the command was successful
            if ($output === null) {
                // If shell_exec returns null, it means the command failed
                echo "Error: Failed to set API key.";
            } else {
                // Output success message
                echo "API key loaded successfully.";
            }

            // Break the loop when the API key is found
            break;
        }
    }

    // If the loop completes without finding the username, output an error message
    if (!isset($apiKey)) {
        echo "No API key found for the provided username.";
    }
} else {
    echo "Error: Unable to retrieve data from the database.";
}
?>
