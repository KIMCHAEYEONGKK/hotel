public int emailCheck(String email) {

  int cnt = userMapper.emailCheck(email);
  System.out.println("cnt:" + cnt);

  return cnt;
}