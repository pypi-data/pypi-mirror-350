from bisslog import BasicUseCase, use_case


class ThirdUseCase(BasicUseCase):

    @use_case
    def custom_name_use_case(self, something: str, *args, **kwargs):

        self.log.info(something)
        self.log.info(args)
        self.log.info(kwargs)
        return 89


THIRD_USE_CASE = ThirdUseCase()
