SELECT c.id
FROM conversations c
JOIN conversation_members m1 ON c.id = m1.conversation_id
JOIN conversation_members m2 ON c.id = m2.conversation_id
WHERE c.is_group = FALSE
  AND m1.user_id = ?
  AND m2.user_id = ?
GROUP BY c.id
HAVING COUNT(DISTINCT m1.user_id || m2.user_id) = 2;
