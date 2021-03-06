import parse_pdf
import augment
import aggregate

from common import arg_parser


if __name__ == "__main__":
  args = arg_parser()

  if args.crawl:
    parse_pdf.main()
    augment.main()
  aggregate.main()
