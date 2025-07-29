CONFIG_YML = '''\
biolib_version: 2

modules:
    main:
        image: 'dockerhub://python:3.9-slim'
        command: |
            python3 -c "
            import argparse
            parser = argparse.ArgumentParser()
            parser.add_argument('--name')
            args = parser.parse_args()
            print(f'Hello there, {args.name}!')
            "
        working_directory: /home/biolib/
        input_files:
            - COPY / /home/biolib/
        output_files:
            - COPY /home/biolib/ /

arguments:
    -
        default_value: Charles Darwin
        description: What is your name?
        key: '--name'
        key_value_separator: ' '
        required: true
        type: text

'''
