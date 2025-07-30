# To convert from cached_openai to abf_openai

  - Rename the folder under src from `cached_openai` to `abf_openai`
  - Add the cache in that folder
  - Add this to the `__init__` function of `CachedClient`
    ```
        # If we're calling this directly (i.e., if the stem is []), ensure the key is an abf key
        # and print a warning in re: the intermediate server
        if (self._api_key is not None) and (len(self._stem) == 0):        
            if not api_key.startswith('abf'):
                raise BaseException('\nYou are trying to use this library with an OpenAI key. You should not provide\n'
                                    'your OpenAI key to any library other than the official openai library. This\n'
                                    'library is only meant to be used with an "AI in Business and Finance" API key,\n'
                                    'which will always start wtih the characters "abf-".')

            print('WARNING : You are making a request via the "AI in Business and Finance" server. These\n'
                  '          requests may be logged. Do *NOT* make any requests with confidential or\n'
                  '          sensitive data.')
    ```
  - Line starting `ValueError('Your request `, remove references to OpenAI
  - Right below that, set the base_url
  - In pyproject.toml
      * Change the pacakge name to abf_openai
      * Update the version
      * Update the description
      * Update the URLs