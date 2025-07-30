![GBShiels](https://raw.githubusercontent.com/SyloraQ/SyloraQ/main/Ast/SQ.png)

pip install SyloraQ

1. **`wait(key="s", num=1)`**: Pauses execution for a specified amount of time. The unit is controlled by the `key` parameter, which can be 's' for seconds, 'm' for minutes, or 'h' for hours.

2. **`ifnull(value, default)`**: This function checks if the given `value` is missing or empty. If it is, the function returns the provided `default` value. Otherwise, it returns the original value.

3. **`switch_case(key, cases, default=None)`**: This function looks up the `key` in the given dictionary of cases. If the `key` exists, it returns the corresponding value. If the value is a callable (like a function), it is executed. If the `key` is not found, it returns the `default` value.

4. **`timer_function(func, seconds)`**: Executes the function `func` after waiting for a specified number of seconds.

5. **`iftrue(var, function)`**: If `var` is `True`, it calls the function `function`.

6. **`iffalse(var, function)`**: If `var` is `False`, it calls the function `function`.

7. **`replace(string, replacement, replacement_with)`**: Replaces occurrences of `replacement` in the string with `replacement_with`.

8. **`until(function, whattodo)`**: Repeatedly executes `whattodo()` until `function()` evaluates to `True`.

9. **`repeat(function, times)`**: Executes the function `function` a specified number of times.

10. **`oncondit(condition, function_true, function_false)`**: Executes `function_true` if `condition` is `True`, else it executes `function_false`.

11. **`repeat_forever(function)`**: Continuously executes `function` indefinitely.

12. **`safe_run(func, *args, **kwargs)`**: Safely runs a function `func`, catching and printing any exceptions that may occur.

13. **`start_timer(seconds, callback)`**: Calls `callback` after waiting for `seconds` seconds.

14. **`generate_random_string(length=15)`**: Generates a random string of alphanumeric characters and symbols of the specified `length`.

15. **`get_ip_address()`**: Returns the local IP address of the machine.

16. **`send_email(subject, body, to_email, mailname, mailpass)`**: Sends an email using Gmail's SMTP server. Requires a Gmail account's username and password.

17. **`generate_unique_id()`**: Generates and returns a unique ID using `uuid`.

18. **`start_background_task(backtask)`**: Starts a function `backtask` in a separate thread, allowing it to run in the background.

19. **`nocrash(func)`**: A decorator that wraps a function `func` to ensure it doesn't crash. If an error occurs, it is caught and logged.

20. **`parallel(*functions)`**: Executes multiple functions in parallel by running them in separate threads.

21. **`gs(func)`**: Returns the source code of the function `func` as a string.

22. **`Jctb(input_string)`**: Converts a string into its binary representation, where each character is represented by a 10-bit binary value.

23. **`Jbtc(binary_input)`**: Converts a binary string (produced by `Jctb`) back to its original string.

24. **`encode_base64(data)`**: Encodes a string `data` into its Base64 representation.

25. **`decode_base64(encoded_data)`**: Decodes a Base64 encoded string back to its original string.

26. **`reverse_string(string)`**: Reverses the input string.

27. **`calculate_factorial(number)`**: Recursively calculates the factorial of a number.

28. **`generate_random_string(length=15)`**: (Defined twice, see above.)

29. **`swap_values(a, b)`**: Swaps the values of `a` and `b` and returns the swapped values.

30. **`replace(string, old, new)`**: (Defined twice, see above.)

31. **`find_maximum(numbers)`**: Finds and returns the maximum value in a list of numbers.

32. **`find_minimum(numbers)`**: Finds and returns the minimum value in a list of numbers.

33. **`sum_list(lst)`**: Returns the sum of elements in the list `lst`.

34. **`reverse_list(lst)`**: Returns the reverse of the list `lst`.

35. **`is_prime(n)`**: Returns `True` if `n` is a prime number, otherwise returns `False`.

36. **`split_into_chunks(text, chunk_size)`**: Splits a string `text` into chunks of size `chunk_size`.

37. **`unique_elements(lst)`**: Returns a list of unique elements from the input list `lst`.

38. **`calculate_average(numbers)`**: Returns the average of a list of numbers.

39. **`calculate_median(numbers)`**: Returns the median of a list of numbers.

40. **`count_words(text)`**: Counts and returns the number of words in the input string `text`.

41. **`count_sentences(text)`**: Counts and returns the number of sentences in the input string `text`.

42. **`add_commas(input_string)`**: Adds commas between characters in the input string.

43. **`remove_spaces(text)`**: Removes all spaces from the input string `text`.

44. **`calculate_square_root(number)`**: Approximates the square root of `number` using the Newton-Raphson method.

45. **`find_files_by_extension(directory, extension)`**: Returns a list of files in the directory that have the specified file extension.

46. **`get_curr_dir()`**: Returns the current working directory.

47. **`check_if_file_exists(file_path)`**: Checks if a file exists at `file_path`.

48. **`monitor_new_files(directory, callback)`**: Continuously monitors the directory for new files and calls `callback` whenever new files are added.

49. **`get_system_uptime()`**: Returns the system's uptime in seconds.

50. **`get_cpu_templinux()`**: Retrieves the CPU temperature on a Linux system.

51. **`monitor_file_changes(file_path, callback)`**: Monitors the file for changes and calls `callback` when the file is modified.

52. **`write_to_file(filename, content)`**: Writes the `content` to the specified `filename`.

53. **`read_from_file(filename)`**: Reads and returns the content of the file specified by `filename`.

54. **`parse_json(json_string)`**: Parses a JSON string and returns the corresponding Python object.

55. **`create_file_if_not_exists(filename)`**: Creates a file if it doesn't already exist.

56. **`create_directory(directory)`**: Creates the specified directory if it doesn't exist.

57. **`get_cpu_usage()`**: Returns the current CPU usage percentage using `psutil`.

58. **`get_memory_usage()`**: Returns the current memory usage percentage using `psutil`.

59. **`create_zip_file(source_dir, output_zip)`**: Creates a ZIP archive of the specified `source_dir`.

60. **`extract_zip_file(zip_file, extract_dir)`**: Extracts a ZIP archive to the specified `extract_dir`.

61. **`move_file(source, destination)`**: Moves a file from `source` to `destination`.

62. **`copy_file(source, destination)`**: Copies a file from `source` to `destination`.

63. **`show_file_properties(file_path)`**: Displays properties of a file (size and last modified time).

64. **`start_http_server(ip="0.0.0.0", port=8000)`**: Starts a simple HTTP server on the given `ip` and `port`.

65. **`stop_http_server()`**: Stops the running HTTP server.

66. **`get_server_status(url="http://localhost:8000")`**: Checks if the server at the given URL is up and running.

67. **`set_server_timeout(timeout=10)`**: Sets the timeout for server connections.

68. **`upload_file_to_server(file_path, url="http://localhost:8000/upload")`**: Uploads a file to a server at the specified URL.

69. **`download_file_from_server(file_url, save_path)`**: Downloads a file from the server and saves it to `save_path`.

70. **`CustomRequestHandler`**: A custom request handler for the HTTP server that responds to specific paths ("/" and "/status").

71. **`start_custom_http_server(ip="0.0.0.0", port=8000)`**: Starts a custom HTTP server using the `CustomRequestHandler`.

72. **`set_server_access_logs(log_file="server_access.log")`**: Configures logging to store server access logs.

73. **`get_server_logs(log_file="server_access.log")`**: Retrieves and prints the server access logs.

74. **`restart_http_server()`**: Restarts the HTTP server.

75. **`check_internet_connection()`**: Checks if the system has internet connectivity by pinging `google.com`.

76. **`create_web_server(directory, port=8000)`**: Serves the contents of a directory over HTTP on the specified port.

77. **`create_custom_web_server(html, port=8000)`**: Serves custom HTML content over HTTP on the specified port.

78. **`JynParser(rep)`**: Executes a Python script passed as `rep` in a new context (using `exec()`).

79. **`contains(input_list, substring)`**: Checks if the given `substring` exists within any element of `input_list`.  

80. **`Jusbcam(Device_Name)`**: Scans connected USB devices and checks if `Device_Name` is present in the list of detected devices.

81. **`claw()`**: Claw allows you to create a custom HTTP server with extensive control over its settings. Here are the things you can customize:
    HTML Code – Modify the webpage content as needed.
    IP Address – Choose which IP the server runs on.
    Port – Set the specific port for the server.
    Subdomains – Configure custom subdomains.
    Return Server Logs – Enable or disable server log reporting.

 82. **`ConsoleCam()`**: Lets you record and return the new changes in the console for a specific part.

 83. **`prn()`**: A faster printing function that mimics the `print()` function, but with quicker execution.

 84. **`Key(Key goes in here)`**  
    - **`press()`**: Simulates pressing the assigned key.
    - **`release()`**: Simulates releasing the assigned key.
    - **`tap()`**: Simulates pressing and releasing the assigned key.
    - **`type_text(Text goes in here instead)`**: Simulates typing the assigned text.
    - **`press_combo(tuple of keys goes in here)`**: Simulates pressing the assigned keys.

 85. **`copy_to_clipboard(text)`**: Copies the given `text` to the clipboard.

 86. **`count_occurrences(lst, element)`**: Counts the occurrences of `element` in the list `lst`.

 87. **`get_curr_time()`**: Returns the current date and time in the format `YYYY-MM-DD HH:MM:SS`.

 88. **`is_palindrome(s)`**: Checks if the string `s` is a palindrome (same forward and backward).

 89. **`get_min_max(list)`**: Returns the minimum and maximum values from the list.

 90. **`is_digits(input)`**: Checks if the `input` is a string consisting only of digits.

 91. **`create_dict(keys, values)`**: Creates a dictionary by pairing elements from `keys` and `values`.

 92. **`square_number(input)`**: Returns the square of the number `input`.

 93. **`get_file_size(file_path)`**: Gets the size of the file at `file_path`.

 94. **`find_duplicates(lst)`**: Finds and returns duplicate elements from the list `lst`.

 95. **`get_average(list)`**: Calculates the average of the numbers in the list.

 96. **`divide(a, b)`**: Divides `a` by `b` and handles division by zero.

 97. **`extract_numbers(s)`**: Extracts all numbers from the string `s`.

 98. **`BinTrig`**:

      1. **exit(root,trig)**: This method binds the window's close event to a custom function (`trig`). It's triggered when the user attempts to close the window.

      2. **mouse_in(root,trig)**: It triggers a given function when the mouse enters the window area (`<Enter>` event).

      3. **mouse_out(root,trig)**: Similar to `mouse_in`, but triggers the function when the mouse leaves the window area (`<Leave>` event).

      4. **fullscreen(root,trig)**: This method checks whether the window is in fullscreen mode by comparing its size with the screen resolution. If the window is fullscreen, the specified function (`trig`) is called.

      5. **minimized(root,trig)**: This method checks if the window is minimized (iconic) or withdrawn, triggering the specified function if the condition is true.

      6. **width_height(root,widmin,heimin,trig)**: This method checks if the window's width or height exceeds specified minimum values (`widmin` and `heimin`). If so, it triggers the given function.

      7. **key_press(root,key,trig)**: It binds a key press event (`<KeyPress-{key}>`) to a specific function (`trig`), where `{key}` is the key to be pressed.

      8. **focus_gain(root,trig)**: This triggers the given function when the window or widget gains focus.

      9. **focus_loss(root,trig)**: This triggers the given function when the window or widget loses focus.

      10. **window_move(root,trig)**: It binds the window's movement event to trigger a custom function whenever the window is moved.

      11. **resize(root,trig)**: Similar to `window_move`, but this event is triggered whenever the window is resized.

      12. **close_shortcut(root,trig)**: Binds the `Alt+F4` shortcut key to close the window and trigger the specified function.

      13. **mouse_button_press(root,button,trig)**: This triggers a function when a specified mouse button is pressed (`<Button-{button}>`).

      14. **mouse_button_release(root,button,trig)**: Similar to `mouse_button_press`, but it triggers when the specified mouse button is released.

      15. **double_click(root,trig)**: This triggers a function when the user double-clicks the left mouse button (`<Double-1>`).

      16. **mouse_motion(root,trig)**: It binds the mouse motion event (`<Motion>`) to trigger a function whenever the mouse moves over the window.

      17. **window_minimized(root,trig)**: Checks if the window is minimized (iconic state) and triggers the specified function if true.

      18. **window_maximized(root,trig)**: This triggers the given function if the window is maximized.

      19. **window_restored(root,trig)**: This triggers when the window is restored to its normal state (not minimized or maximized).

      20. **mouse_wheel_scroll(root,trig)**: It triggers a function when the user scrolls the mouse wheel over the window.

      21. **text_change(root,trig)**: This triggers the given function when text is changed in a widget, such as when a key is released in a text input field.

      22. **focus_on_widget(widget,trig)**: This binds the focus-in event to trigger a function when the widget gains focus.

      23. **focus_off_widget(widget,trig)**: This binds the focus-out event to trigger a function when the widget loses focus.

 99. **`ByteJar`**: Sets/Deletes/Gets Cookie with a 3rd party lightweight program: [Click to download](https://www.mediafire.com/file/cwaa748it4x94jo/ByteJarinstaller.exe/file)

 100. **`letterglue(str="", *substr, str2="")`**: Joins strings and substrings into one.

 101. **`letterglue_creator(word)`**: Generates code to convert each letter of a word into variables and joins them using `letterglue`.

 102. **`Baudio("filename=audio_data", mode="Write", duration=5, Warn=True)`**: Records audio for a specified duration and saves it to a `.Bau` file, returns it or plays the audio if saved. Requires a lightweight program: [Click to download](https://www.mediafire.com/file/qxrtrpr98w53c5w/ByteAUinstaller.exe/file)
 Usage: `Baudio(filename="my_recording", mode="Write", duration=5, Warn=True)`
 
 103. **Btuple**:
      1. **`Btuple.count(*words)`**: Returns the total number of words provided.
      2. **`Btuple.get(index, *words)`**: Retrieves the word at the specified index from the collection.
      3. **`Btuple.exists(item, *words)`**: Checks if the specified item exists in the collection of words.
      4. **`Btuple.first(*words)`**: Returns the first word in the collection, or an error message if empty.
      5. **`Btuple.last(*words)`**: Returns the last word in the collection, or an error message if empty. 

 104. **`isgreater(*nums)`**: Compares two numbers and returns `True` if the first is greater than the second. Displays an error if the input is invalid.  

 105. **`runwfallback(func, fallback_func)`**: Executes `func()` and, if it fails, runs `fallback_func()` instead.  

 106. **`retry(func, retries=3, delay=1)`**: Tries running `func()` multiple times, pausing between attempts. Returns `None` if all attempts fail.  

 107. **`fftime(func)`**: Measures and prints the execution time of `func()`.  

 108. **`debug(func)`**: Logs the function call, arguments, and return value for debugging.  

 109. **`paste_from_clipboard()`**: Retrieves and returns text stored in the system clipboard.  

 110. **`watch_file(filepath, callback)`**: Monitors `filepath` for changes and triggers `callback()` when modified.  

 111. **`is_website_online(url)`**: Checks if the given `url` is reachable and returns `True` if the site is online.  

 112. **`shorten_url(long_url)`**: Generates and returns a shortened version of `long_url`.  

 113. **`celsius_to_fahrenheit(c)`**: Converts temperature `c` from Celsius to Fahrenheit.  

 114. **`fahrenheit_to_celsius(f)`**: Converts temperature `f` from Fahrenheit to Celsius.  

 115. **`efv(string)`**: efv = (exec for variables) : Parses `string` in the code. U can use it like `parser = efv("x=5,y=2");print(parser['y'])` `Out:2` and if parser['x'] it'd return 5

 116. **`Hpass(limit=30)`**: Generates a strong, hard-level password with a length specified by `limit`.

 117. **`l(input)`**: Returns a list of the input.

 118. **`dl(input)`**: Returns the string of the list input.

 119. **`mix(input)`**: Returns the mix of the input.

 120. **`sugar(input)`**: Sugars `(Super Salts)` the input.

 121. **`get_type(value)`**: Returns the type and string representation of the provided value.

 122. **`Cache` Class**: A simple caching system to store and retrieve key-value pairs.

 123. **`cantint(egl, ftw, tw)`**: Performs comparisons on values based on the provided parameters and clears the `tw` list if certain conditions are met.

 124. **`flatten(obj)`**: Flattens a nested list (or iterable) into a single iterable.

 125. **`memoize(func)`**: Caches the result of a function to optimize performance.

 126. **`chunk(iterable, size)`**: Breaks down a large iterable (e.g., list, string) into smaller chunks of a specified size.

 127. **`merge_dicts(*dicts)`**: Merges multiple dictionaries into one.

 128. **`deep_equal(a, b)`**: Checks if two objects (lists or dictionaries) are deeply equal.

 129. **`split_by(text, size)`**: Splits a string into chunks of a given size.

 130. **`GoodBye2Spy` Class**: A class that encapsulates several password and data processing techniques for security-related tasks.

 131. **`Passworded` (Method inside `GoodBye2Spy`)**: Provides functionality for creating and verifying password hashes with key mixing and randomization.

 132. **`Shifting` (Method inside `GoodBye2Spy`)**: Implements a hashing function that uses bitwise operations on the input data.

 133. **`Oneway` (Method inside `GoodBye2Spy`)**: Creates a one-way hashed value using a combination of key mixing and a shifting hash technique.

 134. **`slc(code: str)`**: Strips and parses the provided Python code to remove unnecessary line breaks and spaces.

 135. **`AI(text,questions=None,summarize_text=False,summary_length=3)`**: It can answer questions or summarize the `text`.

 136. **`GAI` (Method inside `AI`)**: It can answer and summarize text.(Better than `summarize` when it comes to QA.)

 137. **`summarize` (Method inside `AI`)**: It can summarize text.(Better than `GAI` when it comes to summarizing.)

 138. **`requireADMIN(For windows only!)`**: Shuts the program with a error when opened if not runned as Administrator.

 139. **`__get_raw_from_web(url)`**: Returns the raw text in the raw text `url` (**Module**).

 140. **`@private`**: Wraps the function and the wrapped function can only used within the class its used.

 141. **`OTKeySystem`**: A class that can verify user without needing a database. *Has web version.*

 142. **`creator(timestamp=25)` (Method inside `OTKeySystem`)**: Generates one time usable,location and program reopen proof key.

 143. **`verifier(key,timestamp=25)` (Method inside `OTKeySyntem`)**: Can verify key generated by `creator` without any database(`timestamp` must be the same!).

 144. **`remove(input,*chars)`**: Removes all elements from `chars` list if existed in input text.

 145. **`get_screen_size()`**: Returns screen size (width,height).

 146. **`NCMLHS(data: str, shift_rate1=3, shift_rate2=5, rotate_rate1=5, rotate_rate2=7, bits=64)`**: Shifts rotates shifts and rotates the data again.

 147. **`remove_duplicates(lst)`**: Removes all duplicates from `lst` list if exists.

 148. **`uncensor(input)`**: Uncensors the censored content from the `input` text such as `H311@` to `Hello` (It can snipe the right answer with the accuracy of 85%).

 149. **`BendableLists`**: A class for managing multiple named lists that can be created, extended, or queried dynamically.

 150. **`create(list_name)` (Method inside `BendableLists`)**: Initializes a new empty list with the specified name, unless it already exists.

 151. **`add(list_name, *elements)` (Method inside `BendableLists`)**: Adds one or more elements to the specified list if it exists.

 152. **`remove(list_name, element)` (Method inside `BendableLists`)**: Removes a specific element from a named list, if both the list and element exist.

 153. **`get(list_name)` (Method inside `BendableLists`)**: Retrieves the contents of a list by name; returns `None` if the list doesn't exist.

 154. **`Nexttime(func, func2)`**: Executes `func` the first time it's called, then alternates with `func2` on subsequent calls using a toggled internal state key (`"runnext"`).
 
 155. **`Http`**: A class that can get and post requests to web.

 156. **`get` (Method inside `Http`)**: Returns scraped data from url.

 157. **`post` (Method inside `Http`)**: Posts a request to a url and returns the response.

 158. **`getos()`**: Returns the os where the script runs.

 159. **`str2int(input)`**: Returns char locations in alphabet based on `input` such as `abc` to `123` or `acb` to `132`.

 160. **`int2str(input)`**: Does the opposite of `str2int`.

 161. **`shiftinwin(shiftrate,text)`**: Shifts `text` with the rate of `shiftrate` and returns it such as shiftinwin(5,Hii) >>> Hii > iiH > iHi > Hii > iiH.

 162. **`runwithin(code,call,params)`**: Runs the `code` calling `class > function() or class.function()` with the `params` placed in such as runwithin(code,func(params go in here when executed dont add params here!) or class.func(params go in here when executed dont add params here!),params). 

 163. **`Locker`**: A class that can lock or unlock a string based on key.(Numbers isn't supported)
 
 164. **`Lock` (Method inside `Locker`)**: Locks the `data` based on `key` and returns it.
 
 165. **`Unlock` (Method inside `Locker`)**: Unlocks the `Ldata` with `Key` and returns it.