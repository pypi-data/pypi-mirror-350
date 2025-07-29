from bisslog import use_case, domain_context, transaction_manager, bisslog_upload_file


log = domain_context.tracer

@use_case
def my_second_use_case(value: float, product_type: str, *args, **kwargs) -> float:

        log.info(
            "Received %d %s", value, transaction_manager.get_component(),
            checkpoint_id="second-reception")

        if product_type == "string1":
            new_value = value * .2
        elif product_type == "string2":
            new_value = value * .3
        elif product_type == "string3":
            new_value = value * .5
        else:
            new_value = value * .05

        uploaded = bisslog_upload_file.main.upload_file_from_local("./test.txt", "/app/casa/20")

        if uploaded:

            log.info("Uploaded file component: %s", transaction_manager.get_component(),
                     checkpoint_id="uploaded-file")

        return new_value
