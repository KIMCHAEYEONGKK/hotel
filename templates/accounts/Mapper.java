@Select("select COUNT(email) from dbelle.user where email=#{email}")
int emailCheck(String email);