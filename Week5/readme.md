# Week 5 Assignment

**Simple Practice with MySQL**

### Task 2: Create database and table in your MySQL server

- Create a new database named website.

  ```sql
  CREATE DATABASE website;
  ```

  ![Create database website](Task2/Create_websit_DB.png)

- Create a new table named member, in the website database.

  ```sql
  CREATE TABLE member (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    follower_count INT UNSIGNED NOT NULL DEFAULT 0,
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
  ```

  ![Create member table](Task2/Create_member_table.png)

  ![Table description](Task2/Member_table_description.png)

### Task 3: SQL CRUD

- INSERT a new row to the member table where name, username and password must
  be set to test. INSERT additional 4 rows with arbitrary data.

  ```sql
  INSERT INTO member (name, username, password)
  VALUES
  ('test','test','test'),
  ('Andy', 'Andy', 123),
  ('Judy', 'Judy', 123),
  ('Betty', 'Betty', 123),
  ('Adam', 'Adam', 123);
  ```

  ![Insert 5 row in member table](Task3/Inser_into_columns.png)

- SELECT all rows from the member table.

  ```sql
  SELECT * FROM member;
  ```

  ![Member table result](Task3/Inser_into_column_result.png)

- SELECT all rows from the member table, in descending order of time.

  ```sql
  SELECT * FROM member ORDER BY time DESC;
  ```

  ![Member table order by time](Task3/table_column_order_by_time_desc.png)

- SELECT total 3 rows, second to fourth, from the member table, in descending order
  of time.

  ```sql
  SELECT * FROM member ORDER BY time DESC LIMIT 3 OFFSET 1;

  ```

  ![Member table limit 3 offset 1](Task3/Member_table_desc_order_limit_3_offset_1.png)

- SELECT rows where username equals to test.

  ```sql
  SELECT * FROM member WHERE username = 'test';
  ```

  ![Select member table where username equals to 'test'](Task3/Select_row_where_username_test.png)

- SELECT rows where name includes the es keyword.

  ```sql
  SELECT * FROM member WHERE name LIKE '%es%';
  ```

  ![Select row where name includes 'es'](Task3/Select_name_include_es.png)

- SELECT rows where both username and password equal to test.

  ```sql
  SELECT * FROM member WHERE username = 'test' AND password = 'test';
  ```

  ![Select row where name and username equal to 'test'](Task3/member_row_where_username_and_password_test.png)

- UPDATE data in name column to test2 where username equals to test.

  ```sql
  UPDATE member SET name = 'test2' WHERE username = 'test';
  ```

  ![Update name to 'test2' where username equals to test](Task3/Update_name_to_test2_where_username_test.png)

### Task 4: SQL Aggregation Functions

- SELECT how many rows from the member table.

  ```sql
  SELECT COUNT(*) FROM member;
  ```

  ![Select the row count](Task4/Total_row_member.png)

- SELECT the sum of follower_count of all the rows from the member table.

  ```sql
  SELECT SUM(follower_count) FROM member;
  ```

  ![The sum of the follower_count](Task4/Sum_of_follower_count.png)

- SELECT the average of follower_count of all the rows from the member table.

  ```sql
  SELECT AVG(follower_count) FROM member;
  ```

  ![Average of follower_count](Task4/Average_of_follower_count.png)

- SELECT the average of follower_count of the first 2 rows, in descending order of
  follower_count, from the member table.

  ```sql
  WITH top_follower AS (
      SELECT follower_count FROM member ORDER BY follower_count DESC LIMIT 2
    )
  SELECT AVG(follower_count) FROM top_follower;
  ```

  ![Average of First two row of follower_count](Task4/Average_of_first_two_follower_count.png)

### Task 5: SQL JOIN

- Create a new table named message, in the website database.

  ```sql
  CREATE TABLE message(
      id BIGINT PRIMARY KEY AUTO_INCREMENT ,
      member_id BIGINT NOT NULL,
      content VARCHAR(255) NOT NULL,
      like_count INT UNSIGNED NOT NULL DEFAULT 0,
      time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (member_id) REFERENCES 'member' (id)
  );
  ```

  ![Crearte message table](Task5/Create%20message%20table.png)

- SELECT all messages, including sender names. We have to JOIN the member table to get that.

  ```sql
  SELECT message.id, message.member_id, message.content, message.like_count, message.time, member.name
  FROM message
  INNER JOIN member ON message.member_id = member.id;
  ```

  ![Select message table with sender name](Task5/Message_table_with_sender_name.png)

- SELECT all messages, including sender names, where sender username equals to test. We have to JOIN the member table to filter and get that.

  ```sql
  SELECT message.id, message.member_id, message.content, message.like_count, message.time, member.name
  FROM message
  INNER JOIN member ON message.member_id = member.id
  WHERE member.username = 'test';
  ```

  ![Message table row with member username equals to 'test'](Task5/Message_table_where_member_username_test.png)

- Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like
  count of messages where sender username equals to test.

  ```sql
  SELECT member.username, AVG(message.like_count)
  FROM message
  INNER JOIN member ON message.member_id = member.id
  WHERE member.username = 'test';
  ```

  ![Average like_count where username equals to 'test'](Task5/Message_Table_average_like_count_join_member_username_test.png)

- Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like
  count of messages GROUP BY sender username.

  ```sql
  SELECT member.username, AVG(message.like_count)
  FROM message
  INNER JOIN member ON message.member_id = member.id
  GROUP BY member.username;
  ```

  ![Average like_count group by username](Task5/Message_avg_like_count_group_by_username.png)
