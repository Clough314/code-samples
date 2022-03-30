<?php
//error_reporting(E_ALL); ini_set('display_errors', 1);

$search = $_POST['search'];
$sql = new mysqli("cse.unl.edu", "apages", "Wtpt4R", "apages");
$qry = "SELECT c.title, c.description, c.prerequisite, c.creditHours, c.courseNum, s.subjectId, a1.aceNum AS aceNum1, a2.aceNum AS aceNum2 ".
    "FROM Course c JOIN Subject s ON c.subject_fk = s.subject_key ".
    "LEFT JOIN Ace AS a1 ON c.ace_1_fk = a1.ace_key ".
    "LEFT JOIN Ace AS a2 ON c.ace_2_fk = a2.ace_key ".
    "WHERE a1.aceNum LIKE ? ".
    "OR a2.aceNum LIKE ?";

$qry = $sql->prepare($qry);
$qry->bind_param('ss', $search, $search);
$qry->execute();
$result = $qry->get_result();
$sql->close();
while ($row = mysqli_fetch_assoc($result)) {
    $rows[] = array(
        'title' => $row['title'],
        'description' => $row['description'],
        'prerequisite' => $row['prerequisite'],
        'creditHours' => $row['creditHours'],
        'courseNum' => $row['courseNum'],
        'courseName' => $row['subjectId'],
        'ace1' => $row['aceNum1'],
        'ace2' => $row['aceNum2']
    );
}
echo json_encode($rows);
?>