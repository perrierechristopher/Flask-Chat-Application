CREATE FUNCTION CreateUser(Id TEXT, Email VARCHAR(100), PasswordT VARCHAR(50))
BEGIN
  INSERT INTO users(id, email, password)
  VALUES(Id, Email, PasswordT);
END

-- CREATE PROCEDURE FetchConversation
--   @User1 TEXT
--   @User2 TEXT
-- AS
-- BEGIN
--   SELECT c.id
--   FROM conversations c
--   JOIN conversation_members m1 ON c.id = m1.conversation_id
--   JOIN conversation_members m2 ON c.id = m2.conversation_id
--   WHERE c.is_group = FALSE
--     AND m1.user_id = @User1
--     AND m2.user_id = @User2
--   GROUP BY c.id
--   HAVING COUNT(DISTINCT m1.user_id || m2.user_id) = 2;
-- END


