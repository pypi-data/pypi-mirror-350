import patronus

patronus.init()


@patronus.traced()
def main():
    logger = patronus.tracing.logger.get_patronus_logger()
    logger.log(body="abc123")
    logger.log(body={"message": "abc123"})


if __name__ == "__main__":
    main()
