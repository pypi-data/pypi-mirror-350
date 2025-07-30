# -*- coding: utf-8 -*-
import asyncio
import json
import os
import unittest

from agentdev.components.internal.user_search_config_center import (
    LocalUserSearchConfigComponent,
    SearchConfigInput,
    SearchConfigOutput,
    UserSearchConfigComponent,
)


class TestUserSearchConfigComponent(unittest.TestCase):

    def test_arun(self):

        # Initialize the component with mocked config
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config = {"config_dir": current_dir}

        component = LocalUserSearchConfigComponent(config=config)
        with open(os.path.join(current_dir, "pro.json"), "r") as file:
            pro_example = json.load(file)  # Prepare input for arun method
        component.common_search_config["pro"] = pro_example
        input_data = SearchConfigInput(strategy="pro", user_id="user_id_1")

        # Run the arun method asynchronously
        result = asyncio.run(component.arun(input_data))

        # Assertions
        self.assertIsInstance(result, SearchConfigOutput)
        self.assertEqual(result.user_config, {})
        self.assertEqual(result.search_payload, pro_example["search"])


if __name__ == "__main__":
    unittest.main()
