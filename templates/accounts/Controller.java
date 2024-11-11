@RestController
public class EmailController {

	@Autowired
	private UserService userService;

	@PostMapping(value="/email/emailCheckProcess")
	@ResponseBody
	public int emailCheck(@RequestParam("email") String email)  {

		int cnt = userService.emailCheck(email);

		return cnt;

	}
}